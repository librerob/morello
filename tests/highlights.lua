-- Check effective UI colors, real token resolution, diagnostics and theme switches.
vim.opt.runtimepath:prepend(vim.fn.getcwd())
local ok, err = pcall(function()
  vim.cmd("filetype plugin indent on")
  vim.cmd("syntax enable")
  local function hex(value) return string.format("#%06X", value) end
  local function luminance(value)
    local sum = 0
    for index, weight in ipairs({ 0.2126, 0.7152, 0.0722 }) do
      local channel = tonumber(value:sub(index * 2, index * 2 + 1), 16) / 255
      sum = sum + weight * (channel <= 0.04045 and channel / 12.92 or ((channel + 0.055) / 1.055) ^ 2.4)
    end
    return sum
  end
  local function contrast(fg, bg)
    local a, b = luminance(fg), luminance(bg)
    return (math.max(a, b) + 0.05) / (math.min(a, b) + 0.05)
  end
  for _, variant in ipairs({ "dark", "light", "dark" }) do
    vim.o.background = variant
    vim.cmd.colorscheme("morello")
    local p = require("morello").get_palette()
    local values = {}
    for _, value in pairs(p) do
      if type(value) == "string" then values[value] = true end
    end
    for _, value in pairs(p.ansi) do values[value] = true end
    local leaked = {}
    local decorative = {
      LineNr = true, NonText = true, EndOfBuffer = true, Whitespace = true,
      SpecialKey = true, FoldColumn = true, FloatBorder = true, WinSeparator = true,
      PmenuSbar = true, PmenuThumb = true,
    }
    local visible = {
      "Normal", "NormalNC", "NormalFloat", "FloatTitle", "FloatFooter", "MsgArea", "MsgSeparator",
      "StatusLine", "StatusLineNC", "StatusLineTerm", "StatusLineTermNC", "WinBar", "WinBarNC",
      "Pmenu", "PmenuSel", "PmenuKind", "PmenuKindSel", "PmenuExtra", "PmenuExtraSel", "PmenuMatch", "PmenuMatchSel",
      "LineNr", "CursorLineNr", "NonText", "EndOfBuffer", "Whitespace", "SpecialKey", "FoldColumn", "Folded",
      "FloatBorder", "WinSeparator", "Visual", "VisualNOS", "Search", "CurSearch", "IncSearch", "Substitute",
      "QuickFixLine", "Directory", "Title", "Error", "ErrorMsg", "WarningMsg", "ModeMsg", "MoreMsg",
      "Comment", "Constant", "String", "Function", "Identifier", "Keyword", "Type", "Operator", "Delimiter",
      "DiffAdd", "DiffChange", "DiffDelete", "DiffText", "DiffTextAdd", "Added", "Changed", "Removed",
      "LspInlayHint", "LspCodeLens", "LspCodeLensSeparator", "DiagnosticError", "DiagnosticWarn", "DiagnosticInfo", "DiagnosticHint",
    }
    for _, name in ipairs(visible) do
      if vim.fn.hlexists(name) == 1 then
        local attrs = vim.api.nvim_get_hl(0, { name = name, link = false })
        for _, key in ipairs({ "fg", "bg", "sp" }) do
          if attrs[key] and not values[hex(attrs[key])] then
            table.insert(leaked, name .. "." .. key .. "=" .. hex(attrs[key]))
          end
        end
        if attrs.fg and not decorative[name] then
          local fg, bg = hex(attrs.fg), attrs.bg and hex(attrs.bg) or p.bg
          if attrs.reverse then fg, bg = bg, fg end
          assert(contrast(fg, bg) >= 4.5, name .. " contrast " .. contrast(fg, bg))
        end
      end
    end
    assert(#leaked == 0, variant .. " leaked UI colors: " .. table.concat(leaked, ", "))
    local selected = vim.api.nvim_get_hl(0, { name = "PmenuSel", link = false })
    for _, name in ipairs({ "PmenuMatchSel", "PmenuKindSel", "PmenuExtraSel", "TelescopeMatching", "CmpItemAbbrMatch", "BlinkCmpLabelMatch" }) do
      local attrs = vim.api.nvim_get_hl(0, { name = name, link = false })
      assert(contrast(hex(attrs.fg), hex(selected.bg)) >= 4.5, name .. " disappears on a selected row")
    end
    for _, name in ipairs({ "CmpItemAbbr", "BlinkCmpLabel" }) do
      assert(vim.api.nvim_get_hl(0, { name = name, link = false }).bg == nil, name .. " hides the selected row background")
    end
    for _, path in ipairs({ "examples/library.lua", "examples/document.py", "examples/library.ts" }) do
      vim.cmd.edit(path)
      -- The preview samples omit Python comments and TypeScript string literals.
      -- Add them in memory so every reading test exercises those token classes.
      if path == "examples/document.py" then
        vim.api.nvim_buf_set_lines(0, -1, -1, false, { "# Comment fixture" })
      elseif path == "examples/library.ts" then
        vim.api.nvim_buf_set_lines(0, -1, -1, false, { 'const label = "Morello";' })
      end
      vim.bo.modified = false
      vim.bo.syntax = vim.bo.filetype
      vim.cmd("syntax sync fromstart")
      local seen = {}
      for row, line in ipairs(vim.api.nvim_buf_get_lines(0, 0, -1, false)) do
        for column = 1, #line do
          if not line:sub(column, column):match("%s") then
            local id = vim.fn.synIDtrans(vim.fn.synID(row, column, 1))
            local color = vim.fn.synIDattr(id, "fg", "gui")
            if color ~= "" then
              color = color:upper()
              assert(values[color], path .. ":" .. row .. " off-palette token " .. color)
              seen[color] = true
            end
          end
        end
      end
      assert(seen[p.keyword], path .. " did not resolve keywords: filetype=" .. vim.bo.filetype .. " syntax=" .. vim.bo.syntax .. " seen=" .. vim.inspect(seen))
      assert(seen[p.string], path .. " did not resolve strings")
      assert(seen[p.comment], path .. " did not resolve comments")
    end
    local ns = vim.api.nvim_create_namespace("morello-test")
    vim.diagnostic.set(ns, 0, {{ lnum = 0, col = 0, message = "Error fixture", severity = vim.diagnostic.severity.ERROR }})
    local win = vim.diagnostic.open_float(0, { scope = "buffer", focus = false })
    assert(win, "Diagnostic float did not open")
    vim.diagnostic.reset(ns)
    for _, window in ipairs(vim.api.nvim_list_wins()) do
      if vim.api.nvim_win_get_config(window).relative ~= "" then vim.api.nvim_win_close(window, true) end
    end
    vim.cmd("diffthis")
    vim.cmd("diffoff")
    vim.cmd.colorscheme("default")
    vim.cmd.colorscheme("morello")
    assert(vim.g.colors_name == "morello")
  end
end)
if not ok then
  io.stderr:write(tostring(err) .. "\n")
  vim.cmd("cquit 1")
end
print("Morello: effective UI colors, contrast, token resolution and editing states passed")
vim.cmd("qa!")
