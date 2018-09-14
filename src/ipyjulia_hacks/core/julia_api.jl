module JuliaAPI

using Compat
using Compat.REPL
using Compat.Dates
using Compat.Pkg

import PyCall
using PyCall: PyObject, pyjlwrap_new

using Requires


function eval_str(code::AbstractString;
                  scope::Module = Main,
                  filename::AbstractString = "string",
                  auto_jlwrap = true,
                  force_jlwrap = false)
    result = include_string(scope, code, filename)
    if force_jlwrap
        return pyjlwrap_new(result)
    elseif auto_jlwrap
        return _wrap(result)
    end
    return result
end


const NpyNumber = Union{
    (t for t in values(PyCall.npy_typestrs) if t <: Number)...
}


_wrap(obj::Any) = pyjlwrap_new(obj)
# Wrap the object if it is desirable to _not_ invoke PyCall's
# automatic conversion.

_wrap(obj::Union{
    Nothing,
    Integer,
    NpyNumber,            # to exclude ForwardDiff.Dual etc.
    Array{<: NpyNumber},  # ditto
    AbstractString,  # should it be just String?
    Dates.AbstractTime,
    IO,
}) = obj
# It's OK to include some types that are not supported PyCall.  In
# that case, those objects are passed through pyjlwrap_new anyway.
# What should be avoided here is to include some types that would be
# converted by PyCall in an irreversible manner (e.g., Symbol,
# BitArray, etc.).


"""
    wrapcall(f, args...; kwargs...)

Wrap what `f(args...; kwargs...)` returns.
"""
wrapcall(f::Base.Callable, args...; kwargs...) = _wrap(f(args...; kwargs...))


struct WrappingCallback
    o::PyObject
    force::Bool
end

function (f::WrappingCallback)(args...; kwargs...)
    wrap = f.force ? pyjlwrap_new : _wrap
    return f.o(wrap.(args)...; (k => wrap(v) for (k, v) in kwargs)...)
end


set_var(name::String, value) = set_var(Symbol(name), value)

function set_var(name::Symbol, value)
    Base.eval(Main, :($name = $value))
    nothing
end

@static if VERSION < v"0.7-"
    getproperty_str(obj, name) = getfield(obj, Symbol(name))
else
    getproperty_str(obj, name) = getproperty(obj, Symbol(name))
end

@static if VERSION < v"0.7-"
    dir(m::Module; all=true, imported=false) = String.(names(m, all, imported))
    dir(::T; _...) where T = String.(fieldnames(T))
else
    dir(m::Module; kwargs...) = String.(names(m; all=true, kwargs...))
    dir(m; all=true) = String.(propertynames(m, all))
end

struct _jlwrap_type end  # a type that would be wrapped as jlwrap by PyCall

get_jlwrap_prototype() = _jlwrap_type()

pybroadcast(op::String, args...) =
    _pybroadcast(eval(Meta.parse(strip(op))), args...)
pybroadcast(op, args...) = _pybroadcast(op, args...)
_pybroadcast(op, args::AbstractArray...) = op.(args...)
_pybroadcast(op, args...) = op(args...)

struct PySlice
    start
    stop
    step
end

struct PyEllipsis end

pygetindex(x, indices...) =
    getindex(x, convert_pyindices(x, indices)...)
pysetindex!(x, value, indices...) =
    setindex!(x, value, convert_pyindices(x, indices)...)

function convert_pyindices(x, indices)
    if applicable(firstindex, x, 1)
        # arrays
        return convert_pyindex.((x,),
                                process_pyindices(ndims(x), indices),
                                1:length(indices))
    elseif indices isa Tuple{Integer} && applicable(firstindex, x)
        # tuples, etc.
        return (firstindex(x) + indices[1],)
    else
        # dictionaries, etc.
        return indices
    end
end

function process_pyindices(nd, indices)
    colons = repeat([:], inner=nd - length(indices))
    i = findfirst(i -> i isa PyEllipsis, indices)
    if i === nothing
        return (indices..., colons...)
    else
        return (indices[1:i - 1]..., colons..., ndices[i + 1:end]...)
    end
end

convert_pyindex(x, i, ::Int) = i

convert_pyindex(x, i::Integer, d::Int) = firstindex(x, d) + i

function convert_pyindex(x, slice::PySlice, d::Int)
    start = (slice.start === nothing ? 0 : slice.start) + firstindex(x, d)
    stop = slice.stop === nothing ? lastindex(x, d) : slice.stop + 1
    step = slice.step === nothing ? 1 : slice.step
    if step == 1
        return start:stop
    else
        return start:step:stop
    end
end


@static if VERSION < v"0.7-"
    completions(_a...; __k...) = String[]
else
    function completions(string, pos, context_module = Main)
        ret, _, should_complete =
            REPL.completions(string, pos, context_module)
        if should_complete
            return map(REPL.completion_text, ret)
        else
            return String[]
        end
    end
end

"""
    start_repl(; <keyword arguments>)

Start Julia REPL.

# Keyword Arguments
- `interactive::Bool = true`
- `quiet::Bool = true`
- `banner::Bool = false`
- `history_file::Bool = true`
- `color_set::Bool = false`: "color (configuration is already) set"
"""
function start_repl(;
        interactive::Bool = true,
        quiet::Bool = true,
        banner::Bool = false,
        history_file::Bool = true,
        color_set::Bool = false,
        )
    if !(stdout isa Base.TTY)
        error("stdout is not a TTY")
    elseif !(stdin isa Base.TTY)
        error("stdin is not a TTY")
    end
    was_interactive = Base.is_interactive
    try
        # Required for Pkg.__init__ to setup the REPL mode:
        Base.eval(:(is_interactive = $interactive))

        Base.run_main_repl(interactive, quiet, banner, history_file, color_set)
    finally
        Base.eval(:(is_interactive = $was_interactive))
    end
end


function __init__()
    # Don't wrap JuliaPy wrappers
    @require Pandas="eadc2687-ae89-51f9-a5d9-86b5a6373a9c" @eval begin
        _wrap(obj::Pandas.PandasWrapped) = obj
    end
    @require SymPy="24249f21-da20-56a4-8eb1-6a02cf4ae2e6" @eval begin
        _wrap(obj::SymPy.SymbolicObject) = obj
    end
    @require PyPlot="d330b81b-6aea-500a-939a-2ce795aea3ee" @eval begin
        _wrap(obj::PyPlot.Figure) = obj
    end
end

module IOPiper

const orig_stdin  = Ref{IO}()
const orig_stdout = Ref{IO}()
const orig_stderr = Ref{IO}()

function __init__()
    orig_stdin[]  = stdin
    orig_stdout[] = stdout
    orig_stderr[] = stderr
end

"""
If `d` ends with an incomplete UTF8-encoded character, return the number of trailing incomplete bytes.
Otherwise, return `0`.

Taken from IJulia.jl.
"""
function num_utf8_trailing(d::Vector{UInt8})
    i = length(d)
    # find last non-continuation byte in d:
    while i >= 1 && ((d[i] & 0xc0) == 0x80)
        i -= 1
    end
    i < 1 && return 0
    c = d[i]
    # compute number of expected UTF-8 bytes starting at i:
    n = c <= 0x7f ? 1 : c < 0xe0 ? 2 : c < 0xf0 ? 3 : 4
    nend = length(d) + 1 - i # num bytes from i to end
    return nend == n ? 0 : nend
end

function pipe_stream(sender::IO, receiver, buf::IO = IOBuffer())
    try
        while !eof(sender)
            nb = bytesavailable(sender)
            write(buf, read(sender, nb))

            # Taken from IJulia.send_stream:
            d = take!(buf)
            n = num_utf8_trailing(d)
            dextra = d[end-(n-1):end]
            resize!(d, length(d) - n)
            s = String(copy(d))

            write(buf, dextra)
            receiver(s)  # check isvalid(String, s)?
        end
    catch e
        if !isa(e, InterruptException)
            rethrow()
        end
        pipe_stream(sender, receiver, buf)
    end
end

const read_stdout = Ref{Base.PipeEndpoint}()
const read_stderr = Ref{Base.PipeEndpoint}()

function pipe_std_outputs(out_receiver, err_receiver)
    global readout_task
    global readerr_task
    read_stdout[], = redirect_stdout()
    readout_task = @async pipe_stream(read_stdout[], out_receiver)
    read_stderr[], = redirect_stderr()
    readerr_task = @async pipe_stream(read_stderr[], err_receiver)
end

end  # module

end  # module
