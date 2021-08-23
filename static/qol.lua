function _OnInit()
if GAME_ID == 0xF266B00B or GAME_ID == 0xFAF99301 then
	Platform = 0
	Now  = 0x032BAE0
	Save = 0x032BB30
	Sys3 = 0x1CCB300
	Btl0 = 0x1CE5D80
elseif ENGINE_TYPE == 'BACKEND' then
	Platform = 1
	Now  = 0x0714DB8 - 0x56450E
	Save = 0x09A7070 - 0x56450E
	Sys3 = 0x2A59DB0 - 0x56450E
	Btl0 = 0x2A74840 - 0x56450E
end
end

function _OnFrame()
--Start with Dash
WriteShort(Btl0+0x31A6C,0x0000820E)
if ReadShort(Now+0) == 0x030A then
	if Platform == 0 then
		WriteShort(0x1C567C4,0x1E)
		WriteShort(0x1C567C8,0x00)
		if ReadShort(Now+8) == 0x3E then WriteByte(0x035DE08,1) end
	elseif Platform == 1 then
		WriteShort(0x29EACA4-0x56450E,0x1E)
		WriteShort(0x29EACA8-0x56450E,0x00)
		if ReadShort(Now+8) == 0x3E then WriteByte(0x0B6275C-0x56450E,1) end
	end
end

--Fast Hyenas II
if ReadShort(Now+0) == 0x050A and ReadShort(Now+8) == 0x39 then
	if Platform == 0 then
		WriteInt(0x1C4EDB4,0)
		WriteInt(0x1C4EDF4,0)
		if ReadInt(0x1D48EFC) == 135 then WriteInt(0x1D48EFC,236) end
	elseif Platform == 1 then
		WriteInt(0x29E32A0-0x56450E,0)
		WriteInt(0x29E32E0-0x56450E,0)
		if ReadInt(0x2A0D108-0x56450E) == 135 then WriteInt(0x2A0D108-0x56450E,236) end
	end
end

--Oogie Boogie HP Barrier Removal
if ReadShort(Now+0) == 0x090E and ReadShort(Now+8) == 0x37 then
	if Platform == 0 then
		WriteInt(0x1C6C4F0,0)
		WriteInt(0x1C6C288,0)
		WriteInt(0x1C6C020,0)
	elseif Platform == 1 then
		WriteInt(0x2A209E8-0x56450E,0)
		WriteInt(0x2A20770-0x56450E,0)
		WriteInt(0x2A204F8-0x56450E,0)
	end
end

--Fast Gift Wrapping
if Platform == 0 then
	Obj0 = 0x1C94100
elseif Platform == 1 then
	Obj0 = 0x2A22B90 - 0x56450E
end
WriteString(Obj0+0xED70,'F_NM170_XL')
WriteString(Obj0+0xED90,'F_NM170_XL.mset')
WriteString(Obj0+0xEDD0,'F_NM170_XL')
WriteString(Obj0+0xEDF0,'F_NM170_XL.mset')
WriteString(Obj0+0xEE30,'F_NM170_XL')
WriteString(Obj0+0xEE50,'F_NM170_XL.mset')

--Skip Dragon Xemnas
if ReadShort(Now+0) == 0x1D12 then
	if Platform == 0 then
		WriteInt(0x1C4A648,0x5C)
	elseif Platform == 1 then
		WriteInt(0x29DEAD8-0x56450E,0x5C)
	end
end

end
