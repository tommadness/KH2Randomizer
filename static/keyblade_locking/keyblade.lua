function _OnInit()
    StaticPointersLoaded = false
    CanExecute = false
    kh2libstatus,kh2lib = pcall(require,"kh2lib")
    if not kh2libstatus then
        print("ERROR (Keyblade Locking Lua): KH2-Lua-Library not installed")
        return
    end

    RequireKH2LibraryVersion(1)

    CanExecute = kh2lib.CanExecute
    if not CanExecute then
        return
    end

    OnPC = kh2lib.OnPC
    Now = kh2lib.Now
    Save = kh2lib.Save
    Sys3Pointer = kh2lib.Sys3Pointer
    MSN = kh2lib.MSN
end

--table key is world id. table value is keyblade ID, keyblade save file inventory address
keyTable = {
	[0] = {-1, -1, false},
	[1] = {0x1F2, 0x368D, STT_ENABLED},	--STT 	| Bond of Flame
	[2] = {0x02A, 0x35A2, TT_ENABLED},	--TT  	| Oathkeeper
	[3] = {0x220, 0x3699, COR_ENABLED},	--CoR 	| Winner's Proof
	[4] = {0x1EE, 0x3689, HB_ENABLED},	--HB  	| Sleeping Lion
	[5] = {0x1EA, 0x3685, BC_ENABLED},	--BC  	| Rumbling Rose
	[6] = {0x1E4, 0x367F, OC_ENABLED},	--OC  	| Hero's Crest 
	[7] = {0x1EC, 0x3687, AG_ENABLED},	--AG  	| Wishing Lamp
	[8] = {0x1E1, 0x367C, LOD_ENABLED},	--LoD 	| Hidden Dragon
	[9] = {0x1EF, 0x368A, HAW_ENABLED},	--HAW 	| Sweet Memeories
	[10] = {0x1E7, 0x3682, PL_ENABLED},	--PL  	| Circle of Life
	[11] = {-1, -1, false},
	[12] = {0x1E5, 0x3680, DC_ENABLED},	--DC  	| Monochrome
	[13] = {0x1E5, 0x3680, DC_ENABLED},	--TR  	| Monochrome
	[14] = {0x1ED, 0x3688, HT_ENABLED},	--HT  	| Decisive Pumpkin
	[15] = {-1, -1, false},
	[16] = {0x1E6, 0x3681, PR_ENABLED},	--PR  	| Follow The Wind
	[17] = {0x1E8, 0x3683, SP_ENABLED},	--SP  	| Photon Debugger
	[18] = {0x21F, 0x3698, TWTNW_ENABLED}	--TWTNW | Two Become One
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
	local worldEnabled = keyTable[curWorld][3]

	--return if somehow not a valid key
	if worldEnabled == false or worldKeyInv == -1 or worldKeySav == -1 then
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
