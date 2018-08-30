module JuliaAPI

@static if VERSION >= v"0.7-"
    import REPL
    import Dates
end
import PyCall
using PyCall: PyObject, pyjlwrap_new


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
# Wrap the object if PyCall would convert it to some

_wrap(obj::Union{
    Nothing,
    Integer,
    NpyNumber,            # to exclude ForwardDiff.Dual etc.
    Array{<: NpyNumber},  # ditto
    AbstractString,  # should it be just String?
    Dates.AbstractTime,
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

end  # module
