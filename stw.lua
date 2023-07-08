disp_arr = {}
ticks = 0
wait = false
function onTick()
    if !wait then
        async.httpGet(8888, "/")
        wait = true
    end
end

function onDraw()
    if disp_arr == {} then
        return
    end
    c = 0
    for y = 1, 160 do
        for x = 1,288 do
            c = c+1
            a = disp_arr[c]
            screen.setColor(a,a,a)
            screen.drawRect(x, y,1,1)
        end
    end
end
function httpReply(port, request_body, response_body)
    disp_arr = split("s",response_body)
    wait = false
end

-- 自作split関数
function split(str, delim)
    -- Eliminate bad cases...
    if string.find(str, delim) == nil then
        return { str }
    end

    local result = {}
    local pat = "(.-)" .. delim .. "()"
    local lastPos
    for part, pos in string.gfind(str, pat) do
        table.insert(result, part)
        lastPos = pos
    end
    table.insert(result, string.sub(str, lastPos))
    return result
end