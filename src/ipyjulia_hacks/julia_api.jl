module JuliaAPI

@static if VERSION >= v"0.7-"
    import REPL
    import Dates
end
using PyCall: pyjlwrap_new


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


_wrap(obj::Any) = pyjlwrap_new(obj)
# Wrap the object if PyCall would convert it to some

_wrap(obj::Union{
    Nothing,
    Number,
    Array,
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
    dir(m::Module; all=true, imported=false) = names(m, all, imported)
    dir(::T; _...) where T = fieldnames(T)
else
    dir(m::Module; kwargs...) = names(m; all=true, kwargs...)
    dir(m; all=true) = propertynames(m, private=!all)
end

struct _jlwrap_type end  # a type that would be wrapped as jlwrap by PyCall

get_jlwrap_prototype() = _jlwrap_type()

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
