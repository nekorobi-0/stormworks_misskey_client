off = {0,0,5,10,5}
keys = {{-1,-2,-3,-4,-5,-6,-7,-8,-9,0},{17,23,5,18,20,25,21,9,15,16},{1,19,4,6,7,8,10,11,12},{26,24,3,22,2,14,13,30},{27,27,27,28,28,28,29,29,29}}
key_id = -10
function onTick()
    key_id = -10
    x = input.getNumber(3)
    y = input.getNumber(4)
    for k = 1,5 do
        if k*10-7 <= y and y <= k*10+1 then
            for i=1,10 do
                if i*10-13+off[k]<=x and x<=i*10-5+off[k] then
                    key_id = keys[k][i]
                end
            end
        end
    end
    if not input.getBool(1) then
        key_id = -10
    end
    output.setNumber(1,key_id)
end

function onDraw()
	screen.drawText(0, 5,"1I2I3I4I5I6I7I8I9I0")
    screen.drawText(0, 15,"QIWIEIR|TIYIUIIIOIP")
    screen.drawText(5, 25, "AISIDIFIGIHIJIKIL")
    screen.drawText(10,35,  "ZIXICIVIBINIMI-")
    screen.drawText(5,45,"SPACE|ENTER|CONV")
end
--[0]:0,[1-9]:-1~-9,[a-z]:1-26,space:27,enter:28