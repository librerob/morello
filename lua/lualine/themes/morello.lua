local p = require("morello.palette")
local function mode(accent)
  return {
    a = { fg = p.bg, bg = accent, gui = "bold" },
    b = { fg = p.fg, bg = p.float },
    c = { fg = p.muted, bg = p.panel },
  }
end
return {
  normal = mode(p.func), insert = mode(p.string), visual = mode(p.constant),
  replace = mode(p.error), command = mode(p.keyword),
  inactive = {
    a = { fg = p.muted, bg = p.panel }, b = { fg = p.muted, bg = p.panel },
    c = { fg = p.comment, bg = p.panel },
  },
}
