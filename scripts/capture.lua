-- Run inside Kitty; scripts/capture.sh captures the actual terminal window.
vim.opt.runtimepath:prepend(vim.fn.getcwd())
vim.o.termguicolors = true
vim.o.number = true
vim.o.relativenumber = false
vim.o.cursorline = true
vim.o.signcolumn = "yes:1"
vim.o.laststatus = 2
vim.o.showmode = false
vim.o.showcmd = false
vim.o.ruler = false
vim.o.wrap = false
vim.o.scrolloff = 3
vim.o.shortmess = "filnxtToOFc"
vim.o.winbar = " %f %m"
vim.o.statusline = " NORMAL %=%{&filetype}  %l:%c "
vim.cmd("filetype plugin indent on")
vim.cmd("syntax enable")
vim.cmd.colorscheme("morello")
local view = vim.env.MORELLO_VIEW or "lua"
if view == "python" then
  vim.cmd("edit examples/document.py")
  vim.api.nvim_win_set_cursor(0, { 15, 12 })
else
  vim.cmd("edit examples/library.lua")
  vim.treesitter.start(0, "lua")
end
if view ~= "python" then vim.api.nvim_win_set_cursor(0, { 23, 16 }) end
if view == "ui" then
  vim.fn.setreg("/", "metadata")
  vim.o.hlsearch = true
  local ns = vim.api.nvim_create_namespace("morello-preview")
  vim.diagnostic.set(ns, 0, {
    { lnum = 9, col = 2, end_col = 8, message = "Expected a non-empty document name", severity = vim.diagnostic.severity.ERROR },
    { lnum = 15, col = 12, end_col = 26, message = "Title falls back to the document name", severity = vim.diagnostic.severity.WARN },
  }, { virtual_text = false, signs = true, underline = true })
  local buf = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_buf_set_lines(buf, 0, -1, false, {
    " Error", " Expected a non-empty document name.", "", " Warning",
    " Title falls back to the document name.",
  })
  for row, group in pairs({ [0] = "DiagnosticError", [3] = "DiagnosticWarn" }) do
    local label = vim.api.nvim_buf_get_lines(buf, row, row + 1, false)[1]
    vim.api.nvim_buf_set_extmark(buf, ns, row, 0, {
      end_col = #label, hl_group = group,
    })
  end
  vim.api.nvim_open_win(buf, false, {
    relative = "editor", row = 7, col = 51, width = 43, height = 5,
    style = "minimal", border = "rounded", title = " Diagnostics ",
  })
end
vim.fn.winrestview({ topline = 1 })
vim.defer_fn(function()
  local messages = vim.fn.execute("messages")
  if messages:find("E%d+:") then
    io.stderr:write(messages .. "\n")
    vim.cmd("cquit 1")
    return
  end
  vim.cmd("redraw!")
  vim.fn.writefile({ "ready" }, assert(vim.env.MORELLO_READY))
end, 700)
