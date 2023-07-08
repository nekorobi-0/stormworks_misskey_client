disp_arr = {}
ticks = 0
wait = 3
rb = "abc"
function onTick()
	now = input.getNumber(3) + "," + input.getNumber(4)
    if 0 < wait then
        async.httpGet(8888, "/"+now)
        wait = wait -1
    end
end

function onDraw()
	disp_arr = split(rb,",")
	screen.setColor(255,255,255)
	screen.drawText(20, 20, disp_arr)
    co = 0
	a = 255
	for i = 1, #disp_arr do
		if a == 255 then
			a = 0
		else
			a = 255
		end
		screen.setColor(a,a,a)
        screen.drawRect(co % 288,math.floor(co/288),disp_arr[i],1)
		co = co + disp_arr[i]
    end
    c = 0
end
function httpReply(port, request_body, response_body)
	if port == 8888 then
		rb = response_body
    	wait = wait + 1
	end
end

-- split
function split (inputstr, sep)
    local t={}
    for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
            table.insert(t, str)
    end
    return t
end