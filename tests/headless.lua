-- Run from the repository root with Neovim 0.10+.
vim.opt.runtimepath:prepend(vim.fn.getcwd())
local ok, err = pcall(function()
  for _, path in ipairs(vim.fn.glob("**/*.lua", false, true)) do
    local chunk, message = loadfile(path)
    assert(chunk, message)
  end
  local theme = require("morello")
  local p = require("morello.palette")
  local function color(hex) return tonumber(hex:sub(2), 16) end
  local function hl(name) return vim.api.nvim_get_hl(0, { name = name, link = false }) end
  local function check_lsp_annotations()
    for _, name in ipairs({ "LspInlayHint", "LspCodeLens", "LspCodeLensSeparator" }) do
      local attrs = hl(name)
      assert(attrs.fg == color(p.comment), name .. " must use the readable comment color")
      assert(attrs.bg == nil, name .. " must inherit its background")
      assert(not attrs.italic, name .. " must stay upright with either comment style")
    end
    assert(hl("NonText").fg == color(p.subdued))
  end

  -- Loading from a light environment must still select this dark scheme.
  vim.o.background = "light"
  theme.setup({ italic_comments = true })
  vim.cmd.colorscheme("morello")
  assert(vim.o.background == "dark")
  assert(vim.g.colors_name == "morello")
  assert(vim.o.termguicolors)
  assert(hl("Normal").bg == color(p.bg))
  assert(hl("Normal").fg == color(p.fg))
  assert(hl("NormalFloat").bg == color(p.float))
  assert(hl("@function.call").fg == color(p.func))
  assert(hl("@lsp.type.function").fg == color(p.func))
  assert(hl("Visual").fg == color(p.fg))
  assert(hl("Visual").bg == color(p.selection))
  assert(hl("CurSearch").fg == color(p.search_current_fg))
  assert(hl("CurSearch").bg == color(p.search_current_bg))
  assert(hl("DiagnosticUnderlineError").undercurl)
  assert(hl("DiagnosticUnderlineError").sp == color(p.error))
  assert(hl("DiagnosticSignError").bold)
  assert(not hl("DiagnosticSignWarn").bold)
  assert(hl("ErrorMsg").bold)
  assert(hl("TelescopeMatching").fg == color(p.func))
  assert(hl("NeoTreeNormal").bg == color(p.panel))
  assert(hl("GitSignsDelete").fg == color(p.error))
  assert(hl("@punctuation.bracket").fg == color(p.punctuation))
  local lualine = require("lualine.themes.morello")
  assert(lualine.normal.a.bg == p.func)
  assert(lualine.insert.a.bg == p.string)
  assert(hl("Comment").italic)
  check_lsp_annotations()
  for index = 0, 15 do
    assert(vim.g["terminal_color_" .. index] == p.ansi[index])
  end
  theme.setup({ italic_comments = false })
  vim.cmd.colorscheme("morello")
  assert(not hl("Comment").italic, "Reload must clear previous italics")
  check_lsp_annotations()
end)
if not ok then
  io.stderr:write(tostring(err) .. "\n")
  vim.cmd("cquit 1")
end
print("Morello: loading, reloading, syntax, LSP annotations, diagnostics and terminal colors passed")
vim.cmd("qa!")
