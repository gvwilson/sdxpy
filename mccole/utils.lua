-- utils.lua
-- Shared helpers for the bin/check-*.lua scripts.

local utils = {}

-- Name of the calling program, used in error messages. Each script sets
-- this to its own filename before invoking any of the helpers below.
utils.program = "utils"

-- Fail with an error message.
function utils.fail(msg)
  io.stderr:write(utils.program .. ": " .. msg .. "\n")
  os.exit(2)
end

-- Get keys that are used but have no definition.
function utils.missing_keys(defined_set, used_files)
  local missing = {}
  for _, key in ipairs(utils.sorted_keys(used_files)) do
    if not defined_set[key] then
      missing[#missing + 1] = key
    end
  end
  return missing
end

-- Open a file or fail with an error message.
function utils.open_file(path)
  local f = io.open(path, "r")
  if not f then
    utils.fail("cannot open " .. path)
  end
  return f
end

-- Read file content as one chunk.
function utils.read_file(path)
  local f = utils.open_file(path)
  local content = f:read("*a")
  f:close()
  return content
end

-- Report used-but-undefined keys under 'label'.
-- Return true if any were found.
function utils.report_missing(defined_set, used_files, label)
  local missing = utils.missing_keys(defined_set, used_files)
  if #missing == 0 then
    return false
  end
  print(label)
  for _, key in ipairs(missing) do
    for _, path in ipairs(utils.sorted_keys(used_files[key])) do
      print(("  %s: %s"):format(key, path))
    end
  end
  return true
end

-- Reports defined-but-unused keys under 'label'.
-- Return true if any were found.
function utils.report_unused(defined_order, used_set, label)
  local unused = utils.unused_keys(defined_order, used_set)
  if #unused == 0 then
    return false
  end
  print(label)
  for _, key in ipairs(unused) do
    print("  " .. key)
  end
  return true
end

-- Get the keys of a map as a sorted array.
function utils.sorted_keys(map)
  local keys = {}
  for key in pairs(map) do
    keys[#keys + 1] = key
  end
  table.sort(keys)
  return keys
end

-- Get defined keys that are never used.
function utils.unused_keys(defined_order, used_set)
  local unused = {}
  for _, key in ipairs(defined_order) do
    if not used_set[key] then
      unused[#unused + 1] = key
    end
  end
  return unused
end

-- The whole package.
return utils
