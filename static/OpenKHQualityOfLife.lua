function _OnInit()
if GAME_ID == 0xF266B00B or GAME_ID == 0xFAF99301 then
	Platform = 0
	Now  = 0x032BAE0
	Save = 0x032BB30
	Sys3 = 0x1CCB300
	Btl0 = 0x1CE5D80
elseif ENGINE_TYPE == 'BACKEND' then
	Platform = 1
	Now  = 0x0714DB8 - 0x56454E
	Save = 0x09A7070 - 0x56450E
	Sys3 = 0x2A59DB0 - 0x56450E
	Btl0 = 0x2A74840 - 0x56450E
end
end


function _OnFrame()
--Shorter Day 5
if ReadShort(Now+0) == 0x0B02 and ReadShort(Now+8) == 0x0C then
	WriteShort(Save+0x034C,0x02)
	WriteShort(Save+0x0350,0x0D)
	WriteShort(Save+0x0356,0x13)
	WriteShort(Save+0x0358,0x03)
	WriteShort(Save+0x035C,0x01)
	WriteShort(Save+0x03E8,0x03)
	WriteShort(Save+0x03EC,0x00)
	WriteByte(Save+0x2394,0x1E)
	WriteShort(Save+0x2110,0x00)
	WriteByte(Save+0x1CDD,ReadByte(Save+0x1CDD)|0xC0)
	WriteByte(Save+0x1CDE,ReadByte(Save+0x1CDE)|0x07)
	WriteByte(Save+0x1CEF,ReadByte(Save+0x1CEF)|0x80)
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

--Skip Dragon Xemnas
if ReadShort(Now+0) == 0x1D12 then
	if Platform == 0 then
		WriteInt(0x1C4A648,0x5C)
	elseif Platform == 1 then
		WriteInt(0x29DEAD8-0x56450E,0x5C)
	end
end

--Remove Growth Abilities
WriteByte(Btl0+0x344A5,0x00000000)
WriteByte(Btl0+0x344AD,0x00000000)
WriteByte(Btl0+0x344B5,0x00000000)
WriteByte(Btl0+0x344BD,0x00000000)
WriteByte(Btl0+0x344C5,0x00000000)
WriteByte(Btl0+0x344CD,0x00000000)
WriteByte(Btl0+0x344D5,0x00000000)
WriteByte(Btl0+0x344DD,0x00000000)
WriteByte(Btl0+0x344E5,0x00000000)
WriteByte(Btl0+0x344ED,0x00000000)
WriteByte(Btl0+0x344F5,0x00000000)
WriteByte(Btl0+0x344FD,0x00000000)
WriteByte(Btl0+0x34505,0x00000000)
WriteByte(Btl0+0x3450D,0x00000000)
WriteByte(Btl0+0x34515,0x00000000)
WriteByte(Btl0+0x3451D,0x00000000)
WriteByte(Btl0+0x34525,0x00000000)
WriteByte(Btl0+0x3452D,0x00000000)
WriteByte(Btl0+0x34535,0x00000000)
WriteByte(Btl0+0x3453D,0x00000000)
WriteByte(Btl0+0x34545,0x00000000)
WriteByte(Btl0+0x3454D,0x00000000)
WriteByte(Btl0+0x34555,0x00000000)
WriteByte(Btl0+0x3455D,0x00000000)
WriteByte(Btl0+0x34565,0x00000000)
WriteByte(Btl0+0x3456D,0x00000000)
WriteByte(Btl0+0x34575,0x00000000)
WriteByte(Btl0+0x3457D,0x00000000)
WriteByte(Btl0+0x34585,0x00000000)
WriteByte(Btl0+0x3458D,0x00000000)
WriteByte(Btl0+0x34595,0x00000000)
WriteByte(Btl0+0x3459D,0x00000000)
WriteByte(Btl0+0x345A5,0x00000000)
WriteByte(Btl0+0x345AD,0x00000000)
WriteByte(Btl0+0x345B5,0x00000000)
ValorLv = ReadByte(Save+0x32F6)
WisdmLv = ReadByte(Save+0x332E)
LimitLv = ReadByte(Save+0x3366)
MastrLv = ReadByte(Save+0x339E)
FinalLv = ReadByte(Save+0x33D6)
if ValorLv == 1 or ValorLv == 2 then WriteShort(Save+0x32FC,0x805E)
elseif ValorLv == 3 or ValorLv == 4 then WriteShort(Save+0x32FC,0x805F)
elseif ValorLv == 5 or ValorLv == 6 then WriteShort(Save+0x32FC,0x8060)
elseif ValorLv == 7 then WriteShort(Save+0x32FC,0x8061) end
if WisdmLv == 1 or WisdmLv == 2 then WriteShort(Save+0x3334,0x8062)
elseif WisdmLv == 3 or WisdmLv == 4 then WriteShort(Save+0x3334,0x8063)
elseif WisdmLv == 5 or WisdmLv == 6 then WriteShort(Save+0x3334,0x8064)
elseif WisdmLv == 7 then WriteShort(Save+0x3334,0x8065) end
if LimitLv == 1 or LimitLv == 2 then WriteShort(Save+0x336C,0x8234)
elseif LimitLv == 3 or LimitLv == 4 then WriteShort(Save+0x336C,0x8235)
elseif LimitLv == 5 or LimitLv == 6 then WriteShort(Save+0x336C,0x8236)
elseif LimitLv == 7 then WriteShort(Save+0x336C,0x8237) end
if MastrLv == 1 or MastrLv == 2 then WriteShort(Save+0x33A4,0x8066)
elseif MastrLv == 3 or MastrLv == 4 then WriteShort(Save+0x33A4,0x8067)
elseif MastrLv == 5 or MastrLv == 6 then WriteShort(Save+0x33A4,0x8068)
elseif MastrLv == 7 then WriteShort(Save+0x33A4,0x8069) end
if FinalLv == 1 or FinalLv == 2 then WriteShort(Save+0x33DC,0x806A)
elseif FinalLv == 3 or FinalLv == 4 then WriteShort(Save+0x33DC,0x806B)
elseif FinalLv == 5 or FinalLv == 6 then WriteShort(Save+0x33DC,0x806C)
elseif FinalLv == 7 then WriteShort(Save+0x33DC,0x806D) end

--Summon Animation "None"
if ReadShort(Now+0) == 0x2002 and ReadShort(Now+8) == 0x01 then
    WriteByte(Save+0x41A5,ReadByte(Save+0x41A5)~0x6) --Default No Summon Animations
end
end