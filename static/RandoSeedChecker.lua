local kh2libstatus, kh2lib, can_execute, on_pc, sys3, btl0
local verbose = false
local check_completed = false
local checked_locations_count = 0
local all_valid = true

function _OnInit()
    kh2libstatus, kh2lib = pcall(require, "kh2lib")
    if not kh2libstatus then
        ConsolePrint("(Randomizer Seed Checker): KH2-Lua-Library mod is not installed or failed to initialize", 3)
        ConsolePrint(kh2lib, 3)
        can_execute = false
        return
    end

    Log("Randomizer Seed Checker")
    RequireKH2LibraryVersion(2)

    can_execute = kh2lib.CanExecute
    if not can_execute then
        return
    end

    on_pc = kh2lib.OnPC
end

-- Gets an address within a BAR file.
local function get_bar_address(file, subfile, offset)
    local subpoint = file + 0x08 + 0x10 * subfile
    -- Detect errors
    if ReadInt(file, on_pc) ~= 0x01524142 then         -- Header mismatch
        return 0x0
    elseif subfile > ReadInt(file + 4, on_pc) then     -- Subfile over count
        return 0x0
    elseif offset >= ReadInt(subpoint + 4, on_pc) then -- Offset exceed subfile length
        return 0x0
    end
    return file + (ReadInt(subpoint, on_pc) - ReadInt(file + 8, on_pc)) + offset
end

-- Verifies that the expected_item and actual_item are equal. If not, sets all_valid to false.
local function check_item(expected_item, actual_item, label)
    checked_locations_count = checked_locations_count + 1
    if expected_item ~= actual_item then
        if verbose then
            LogError("[" .. label .. "] does not have expected item " .. expected_item .. " - it has " .. actual_item)
        end
        all_valid = false
    end
end

local function get_chest_item(chest_address)
    -- Found this offset logic via a Discord message, hopefully it's game update-proof
    -- 0x1CCB300 is the address of an unedited 03system.bin, 0x14424 is the offset in the subfile where TRSR starts
    -- Values for chest_address come from https://github.com/1234567890num/KH2FM-Plando-Useful-Codes/wiki/Chests
    local offset = chest_address - 0x1CCB300 - 0x14424
    local address = get_bar_address(sys3, 0x07, offset)
    return ReadShort(address, on_pc)
end

local function check_chest_item(chest_address, expected_item, label)
    check_item(expected_item, get_chest_item(chest_address), label)
end

local function get_popup_item(popup_offset)
    -- Found addresses and offset code here
    -- https://github.com/GhostTheBoo/custom-seed-generator/blob/update-lua-code-generation/src/Data/popupsData.js
    local address = get_bar_address(sys3, 0x07, popup_offset)
    return ReadShort(address, on_pc)
end

local function check_popup_item(popup_offset, expected_item, label)
    check_item(expected_item, get_popup_item(popup_offset), label)
end

-- Note: Bonuses are a bit of a pain - could be an actual stat bonus _or_ an item. TBD if we want to bother.
--local function get_bonus_item(bonus_address)
--end

local function get_level_up_item(level_base_offset)
    -- Found addresses and offset code here
    -- https://github.com/GhostTheBoo/custom-seed-generator/blob/update-lua-code-generation/src/Data/levelData.js
    local sword_offset = level_base_offset + 0x08
    local address = get_bar_address(btl0, 0x05, sword_offset)
    return ReadShort(address, on_pc)
end

local function check_level_up_item(level_base_offset, expected_item, label)
    check_item(expected_item, get_level_up_item(level_base_offset), label)
end

local function get_form_level_item(form_level_base_offset)
    -- Found addresses and offset code here
    -- https://github.com/GhostTheBoo/custom-seed-generator/blob/update-lua-code-generation/src/Data/formsData.js
    local reward_offset = form_level_base_offset + 0x06
    local address = get_bar_address(btl0, 0x10, reward_offset)
    return ReadShort(address, on_pc)
end

local function check_form_level_item(form_level_base_offset, expected_item, label)
    check_item(expected_item, get_form_level_item(form_level_base_offset), label)
end

-- Body of this function is expected to be filled in by the seed generator to add a sampling of checks.
local function check_expected_items()
    -- {REPLACE_ME}
end

function _OnFrame()
    if not can_execute then
        return
    end

    if not check_completed then
        check_completed = true

        -- Note: Loading these pointers in _OnInit is too early
        sys3 = ReadPointer(kh2lib.Sys3Pointer)
        btl0 = ReadPointer(kh2lib.Btl0Pointer)

        check_expected_items()

        if all_valid then
            LogSuccess("All checks passed (checked " .. checked_locations_count .. " locations)")
        else
            LogError("One or more checks failed. Try building again in OpenKH Mods Manager, and make sure your randomizer seed is above the GoA mod.")

            -- TODO: Update the game UI somehow (likely on the "new game") to indicate that things are in a bad state
        end
    end
end
