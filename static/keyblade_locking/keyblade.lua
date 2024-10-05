function GetVersion()
	if (GAME_ID == 0xF266B00B or GAME_ID == 0xFAF99301) and ENGINE_TYPE == "ENGINE" then --PCSX2
		if ENGINE_VERSION < 3.0 then
			print('LuaEngine is Outdated. Things might not work properly.')
		end
		OnPC = false
		GameVersion=1
		Now = 0x032BAE0 --Current Location
		Save = 0x032BB30 --Save File
		Sys3Pointer = 0x1C61AF8 --03system.bin Pointer Address
	elseif GAME_ID == 0x431219CC and ENGINE_TYPE == 'BACKEND' then --PC
		if ENGINE_VERSION < 5.0 then
			ConsolePrint('LuaBackend is Outdated. Things might not work properly.',2)
		end
		OnPC = true
		if ReadString(0x9A9330,4) == 'KH2J' then --EGS
			GameVersion=2
			Now = 0x0716DF8
			Save = 0x9A9330
			Sys3Pointer = 0x2AE58D0
		elseif ReadString(0x09A9830,4) == 'KH2J' then --Steam
			GameVersion=3
			Now = 0x0717008
			Save = 0x9A98B0
			Sys3Pointer = 0x2AE5E50
		else
			ConsolePrint("Unable to detect version of PC running")
		end
	end
end


function _OnInit()
GameVersion = 0
print('Keyblade Locking Lua from Seed Generator')
end

--table key is world id. table value is keyblade ID, keyblade save file inventory address 
keyTable = {
	[0] = {-1, -1},
	[1] = {0x1F2, 0x368D},	--STT 	| Bond of Flame
	[2] = {0x02A, 0x35A2},	--TT  	| Oathkeeper
	[3] = {0x220, 0x3699},	--CoR 	| Winner's Proof
	[4] = {0x1EE, 0x3689},	--HB  	| Sleeping Lion
	[5] = {0x1EA, 0x3685},	--BC  	| Rumbling Rose
	[6] = {0x1E4, 0x367F},	--OC  	| Hero's Crest 
	[7] = {0x1EC, 0x3687},	--AG  	| Wishing Lamp
	[8] = {0x1E1, 0x367C},	--LoD 	| Hidden Dragon
	[9] = {0x1EF, 0x368A},	--HAW 	| Sweet Memeories
	[10] = {0x1E7, 0x3682},	--PL  	| Circle of Life
	[11] = {-1, -1},
	[12] = {0x1E5, 0x3680},	--DC  	| Monochrome
	[13] = {0x1E5, 0x3680},	--TR  	| Monochrome
	[14] = {0x1ED, 0x3688},	--HT  	| Decisive Pumpkin
	[15] = {-1, -1},
	[16] = {0x1E6, 0x3681},	--PR  	| Follow The Wind
	[17] = {0x1E8, 0x3683},	--SP  	| Photon Debugger
	[18] = {0x21F, 0x3698}	--TWTNW | Two Become One
}

function CheckKeyblade(invAdd, keyValue)
    --invAdd = keyblade inventory address in savefile to use
    --keyValue = keyblade item ID
    local Key = ReadShort(Save + 0x24F0)
    local Valor = ReadShort(Save + 0x32F4)
    local Master = ReadShort(Save + 0x339C)
    local Final = ReadShort(Save + 0x33D4)
    local SaveKey = ReadByte(Save + invAdd)

    if (SaveKey > 0 or Key == keyValue or Valor == keyValue or Master == keyValue or Final == keyValue) then
		return true
    end
	
    return false
end

function BAR(File,Subfile,Offset) --Get address within a BAR file
local Subpoint = File + 0x08 + 0x10*Subfile
local Address
--Detect errors
if ReadInt(File,OnPC) ~= 0x01524142 then --Header mismatch
	return
elseif Subfile > ReadInt(File+4,OnPC) then --Subfile over count
	return
elseif Offset >= ReadInt(Subpoint+4,OnPC) then --Offset exceed subfile length
	return
end
--Get address
Address = File + (ReadInt(Subpoint,OnPC) - ReadInt(File+8,OnPC)) + Offset
return Address
end

function _OnFrame()
if GameVersion == 0 then --Get anchor addresses
	GetVersion()
	return
end
if true then --Define current values for common addresses
	World  = ReadByte(Now+0x00)
	Room   = ReadByte(Now+0x01)
	Place  = ReadShort(Now+0x00)
	if Place == 0xFFFF or not MSN then
		if not OnPC then
			Sys3 = ReadInt(Sys3Pointer)
			MSN = 0x04FA440
		else
			Sys3 = ReadLong(Sys3Pointer)
			if ReadString(0x09A92F0,4) == 'KH2J' then --EGS
				MSN = 0x0BF2C40
			elseif ReadString(0x09A9830,4) == 'KH2J' then --Steam
				MSN = 0x0BF3340
			end
		end
	end
end
CanUnlock()
end

function CanUnlock()
	--return if not a valid world
	if (World <= 1 or World >= 19) then
		return
    end
	
	--STT Tutorial Chest/GoA Chests (Always unlocked)
	if Place == 0x2002 or Place == 0x1A04 then
		WriteShort(BAR(Sys3,0x2,0x04BA),0x20,OnPC)
		return
	end
	
	--get world value and set here to modify later if needed (STT/COR)
	local curWorld = World
	
	--STT Check
	if World == 0x2 and ReadByte(Save+0x1CFF) == 13 then --STT/TT
		curWorld = curWorld -1
	end

	--CoR Check
	if World == 0x4 and Room >= 0x15 and Room <= 0x18 then
		curWorld = curWorld -1
	end

	--get key values
	local worldKeyInv = keyTable[curWorld][1]
	local worldKeySav = keyTable[curWorld][2]

	--return if somehow not a valid key
	if worldKeyInv == -1 or worldKeySav == -1 then
		return
	end
	
	--get and set unlock status
	local Unlock = CheckKeyblade(worldKeySav, worldKeyInv)
	
	if Unlock then
		WriteShort(BAR(Sys3,0x2,0x04BA),0x20,OnPC)
	else
		WriteShort(BAR(Sys3,0x2,0x04BA),0x00,OnPC)
	end
end