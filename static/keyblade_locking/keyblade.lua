function _OnInit()
    CanExecute = false
    StaticPointersLoaded = false

    if (GAME_ID == 0xF266B00B or GAME_ID == 0xFAF99301) and ENGINE_TYPE == "ENGINE" then --PCSX2
        if ENGINE_VERSION < 3.0 then
            print('LuaEngine is Outdated. Things might not work properly.')
        end
        OnPC = false
        CanExecute = true
        Now = 0x032BAE0 --Current Location
        Save = 0x032BB30 --Save File
        Sys3Pointer = 0x1C61AF8 --03system.bin Pointer Address
        MSN = 0x04FA440
        print('Keyblade Locking Lua from Seed Generator - PCSX2')
    elseif GAME_ID == 0x431219CC and ENGINE_TYPE == 'BACKEND' then --PC
        if ENGINE_VERSION < 5.0 then
            ConsolePrint('LuaBackend is Outdated. Things might not work properly.',2)
        end
        OnPC = true
        if ReadByte(0x566A8E) == 0xFF then --EGS 1.0.0.9
            CanExecute = true
            Now = 0x0716DF8
            Save = 0x09A92F0
            Sys3Pointer = 0x2AE5890
            MSN = 0x0BF2C40
            ConsolePrint('Keyblade Locking Lua from Seed Generator - EGS 1.0.0.9')
        elseif ReadByte(0x56668E) == 0xFF then --Steam Global "1.0.0.9"
            CanExecute = true
            Now = 0x0717008
            Save = 0x09A9830
            Sys3Pointer = 0x2AE5DD0
            MSN = 0x0BF3340
            ConsolePrint('Keyblade Locking Lua from Seed Generator - Steam Global "1.0.0.9"')
        elseif ReadByte(0x56640E) == 0xFF then --Steam JP "1.0.0.9"
            CanExecute = true
            Now = 0x0716008
            Save = 0x09A8830
            Sys3Pointer = 0x2AE4DD0
            MSN = 0x0BF2340
            ConsolePrint('Keyblade Locking Lua from Seed Generator - Steam JP "1.0.0.9"')
        elseif ReadByte(0x660E44) == 106 then --EGS 1.0.0.10
            CanExecute = true
            Now = 0x0716DF8
            Save = 0x09A9330
            Sys3Pointer = 0x2AE58D0
            MSN = 0x0BF2C80
            ConsolePrint('Keyblade Locking Lua from Seed Generator - EGS 1.0.0.10')
        elseif ReadByte(0x660EF4) == 106 then --Steam "1.0.0.10"
            CanExecute = true
            Now = 0x0717008
            Save = 0x09A98B0
            Sys3Pointer = 0x2AE5E50
            MSN = 0x0BF33C0
            ConsolePrint('Keyblade Locking Lua from Seed Generator - Steam "1.0.0.10"')
        else
            ConsolePrint("Unable to detect version of PC running")
        end
    end
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
    if not CanExecute then
        return
    end

    if not StaticPointersLoaded then
        if not OnPC then
            Sys3 = ReadInt(Sys3Pointer)
        else
            Sys3 = ReadLong(Sys3Pointer)
        end
        StaticPointersLoaded = true
    end

    World  = ReadByte(Now+0x00)
    Room   = ReadByte(Now+0x01)
    Place  = ReadShort(Now+0x00)

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
