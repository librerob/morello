-- Morello: a dependency-free, truecolor Neovim colorscheme.
local M = {}
local options = { italic_comments = false }

function M.setup(opts)
  options = vim.tbl_extend("force", options, opts or {})
end

function M.get_palette()
  local name = vim.o.background == "light" and "morello.palette-light" or "morello.palette"
  return require(name)
end

function M.load()
  local p = M.get_palette()
  package.loaded["lualine.themes.morello"] = nil
  vim.g.colors_name = nil
  vim.o.termguicolors = true
  vim.cmd("highlight clear")
  if vim.fn.exists("syntax_on") == 1 then
    vim.cmd("syntax reset")
  end
  vim.g.colors_name = "morello"

  local groups = {
    Normal = { fg = p.fg, bg = p.bg },
    NormalNC = { fg = p.fg, bg = p.bg },
    NormalFloat = { fg = p.fg, bg = p.float },
    FloatBorder = { fg = p.border, bg = p.float },
    FloatTitle = { fg = p.func, bg = p.float, bold = true },
    WinSeparator = { fg = p.border },
    Cursor = { fg = p.bg, bg = p.cursor },
    lCursor = { fg = p.bg, bg = p.cursor },
    CursorLine = { bg = p.line },
    CursorColumn = { bg = p.line },
    ColorColumn = { bg = p.line },
    LineNr = { fg = p.subdued },
    CursorLineNr = { fg = p.focus, bold = true },
    SignColumn = { bg = p.bg },
    FoldColumn = { fg = p.subdued, bg = p.bg },
    Folded = { fg = p.muted, bg = p.line },
    NonText = { fg = p.subdued },
    EndOfBuffer = { fg = p.subdued },
    Whitespace = { fg = p.subdued },
    SpecialKey = { fg = p.subdued },
    Conceal = { fg = p.muted },
    LspInlayHint = { fg = p.comment },
    LspCodeLens = { fg = p.comment },
    LspCodeLensSeparator = { fg = p.comment },
    Directory = { fg = p.func },
    Title = { fg = p.func, bold = true },

    -- Explicit foreground keeps selected comments and errors readable.
    Visual = { fg = p.fg, bg = p.selection, nocombine = true },
    VisualNOS = { fg = p.fg, bg = p.selection, nocombine = true },
    Search = { fg = p.search_fg, bg = p.search_bg },
    IncSearch = { fg = p.search_current_fg, bg = p.search_current_bg },
    CurSearch = { fg = p.search_current_fg, bg = p.search_current_bg },
    Substitute = { fg = p.bg, bg = p.constant },
    MatchParen = { fg = p.cursor, bold = true, underline = true },

    StatusLine = { fg = p.fg, bg = p.panel },
    StatusLineNC = { fg = p.muted, bg = p.line },
    TabLine = { fg = p.muted, bg = p.line },
    TabLineSel = { fg = p.bg, bg = p.func, bold = true },
    TabLineFill = { bg = p.bg },
    WinBar = { fg = p.fg, bg = p.bg },
    WinBarNC = { fg = p.muted, bg = p.bg },
    Pmenu = { fg = p.fg, bg = p.float },
    PmenuSel = { fg = p.bg, bg = p.func },
    PmenuKind = { fg = p.type, bg = p.float },
    PmenuKindSel = { fg = p.bg, bg = p.func },
    PmenuExtra = { fg = p.muted, bg = p.float },
    PmenuExtraSel = { fg = p.bg, bg = p.func },
    PmenuSbar = { bg = p.line },
    PmenuThumb = { bg = p.subdued },
    WildMenu = { fg = p.bg, bg = p.func },
    QuickFixLine = { fg = p.fg, bg = p.selection },

    Comment = { fg = p.comment, italic = options.italic_comments },
    Constant = { fg = p.constant },
    String = { fg = p.string },
    Character = { fg = p.string },
    Number = { fg = p.constant },
    Boolean = { fg = p.constant },
    Float = { fg = p.constant },
    Identifier = { fg = p.variable },
    Function = { fg = p.func },
    Statement = { fg = p.keyword },
    Conditional = { fg = p.keyword },
    Repeat = { fg = p.keyword },
    Label = { fg = p.keyword },
    Operator = { fg = p.operator },
    Keyword = { fg = p.keyword },
    Exception = { fg = p.keyword },
    PreProc = { fg = p.keyword },
    Include = { fg = p.keyword },
    Define = { fg = p.keyword },
    Macro = { fg = p.func },
    PreCondit = { fg = p.keyword },
    Type = { fg = p.type },
    StorageClass = { fg = p.keyword },
    Structure = { fg = p.type },
    Typedef = { fg = p.type },
    Special = { fg = p.constant },
    SpecialChar = { fg = p.constant },
    Tag = { fg = p.type },
    Delimiter = { fg = p.punctuation },
    SpecialComment = { fg = p.comment },
    Debug = { fg = p.keyword },
    Underlined = { fg = p.string, underline = true },
    Ignore = { fg = p.subdued },
    Error = { fg = p.error, underline = true },
    Todo = { fg = p.bg, bg = p.func, bold = true },
    ErrorMsg = { fg = p.error, bold = true },
    WarningMsg = { fg = p.warning },
    MoreMsg = { fg = p.string },
    ModeMsg = { fg = p.func },
    Question = { fg = p.func },

    DiffAdd = { fg = p.fg, bg = p.diff_add },
    DiffChange = { fg = p.fg, bg = p.diff_change },
    DiffDelete = { fg = p.error, bg = p.diff_delete },
    DiffText = { fg = p.fg, bg = p.diff_text, bold = true },
    Added = { fg = p.focus },
    Changed = { fg = p.type },
    Removed = { fg = p.error },

    ["@variable"] = { link = "Identifier" },
    ["@variable.builtin"] = { fg = p.type },
    ["@variable.parameter"] = { fg = p.variable },
    ["@variable.member"] = { fg = p.variable },
    ["@constant"] = { link = "Constant" },
    ["@constant.builtin"] = { link = "Constant" },
    ["@constant.macro"] = { link = "Constant" },
    ["@module"] = { fg = p.type },
    ["@label"] = { link = "Label" },
    ["@string"] = { link = "String" },
    ["@string.documentation"] = { link = "String" },
    ["@string.regexp"] = { fg = p.constant },
    ["@string.escape"] = { fg = p.constant },
    ["@string.special.url"] = { fg = p.string, underline = true },
    ["@character"] = { link = "Character" },
    ["@boolean"] = { link = "Boolean" },
    ["@number"] = { link = "Number" },
    ["@number.float"] = { link = "Float" },
    ["@type"] = { link = "Type" },
    ["@type.builtin"] = { link = "Type" },
    ["@type.definition"] = { link = "Type" },
    ["@attribute"] = { fg = p.constant },
    ["@property"] = { fg = p.variable },
    ["@function"] = { link = "Function" },
    ["@function.builtin"] = { link = "Function" },
    ["@function.call"] = { link = "Function" },
    ["@function.macro"] = { link = "Function" },
    ["@function.method"] = { link = "Function" },
    ["@function.method.call"] = { link = "Function" },
    ["@constructor"] = { fg = p.func },
    ["@operator"] = { link = "Operator" },
    ["@keyword"] = { link = "Keyword" },
    ["@keyword.operator"] = { link = "Operator" },
    ["@punctuation.delimiter"] = { fg = p.punctuation },
    ["@punctuation.bracket"] = { fg = p.punctuation },
    ["@punctuation.special"] = { fg = p.constant },
    ["@comment"] = { link = "Comment" },
    ["@comment.documentation"] = { link = "Comment" },
    ["@comment.todo"] = { link = "Todo" },
    ["@comment.error"] = { fg = p.error },
    ["@comment.warning"] = { fg = p.warning },
    ["@comment.note"] = { fg = p.info },
    ["@comment.hint"] = { fg = p.hint },
    ["@markup.strong"] = { bold = true },
    ["@markup.italic"] = { italic = true },
    ["@markup.strikethrough"] = { strikethrough = true },
    ["@markup.heading"] = { fg = p.func, bold = true },
    ["@markup.link"] = { fg = p.type, underline = true },
    ["@markup.link.label"] = { fg = p.func, underline = true },
    ["@markup.link.url"] = { fg = p.string, underline = true },
    ["@markup.raw"] = { fg = p.string },
    ["@markup.list"] = { fg = p.keyword },
    ["@tag"] = { fg = p.type },
    ["@tag.attribute"] = { fg = p.variable },
    ["@tag.delimiter"] = { fg = p.operator },
    ["@diff.plus"] = { link = "Added" },
    ["@diff.minus"] = { link = "Removed" },
    ["@diff.delta"] = { link = "Changed" },
  }

  local links = {
    GitSignsAdd = "Added", GitSignsChange = "Changed", GitSignsDelete = "Removed",
    GitSignsAddNr = "Added", GitSignsChangeNr = "Changed", GitSignsDeleteNr = "Removed",
    TelescopeNormal = "NormalFloat", TelescopeBorder = "FloatBorder",
    TelescopeSelection = "PmenuSel", TelescopeMatching = "Function",
    TelescopePromptTitle = "FloatTitle", TelescopeResultsTitle = "FloatTitle",
    TelescopePreviewTitle = "FloatTitle", TelescopePromptPrefix = "Keyword",
    NeoTreeNormal = "NormalFloat", NeoTreeNormalNC = "NormalFloat",
    NeoTreeDirectoryName = "Directory", NeoTreeDirectoryIcon = "Directory",
    NeoTreeFileName = "Normal", NeoTreeRootName = "Title", NeoTreeGitModified = "Changed",
    NeoTreeGitAdded = "Added", NeoTreeGitDeleted = "Removed", NeoTreeIndentMarker = "NonText",
    OilDir = "Directory", OilDirIcon = "Directory", OilFile = "Normal",
    WhichKey = "Function", WhichKeyGroup = "Type", WhichKeyDesc = "NormalFloat",
    WhichKeySeparator = "Delimiter", WhichKeyBorder = "FloatBorder",
    BlinkCmpMenu = "Pmenu", BlinkCmpMenuBorder = "FloatBorder",
    BlinkCmpDoc = "NormalFloat", BlinkCmpDocBorder = "FloatBorder",
    BlinkCmpLabel = "Pmenu", BlinkCmpLabelMatch = "Function", BlinkCmpKind = "Type",
    CmpItemAbbr = "Pmenu", CmpItemAbbrMatch = "Function", CmpItemKind = "Type",
    SnacksNormal = "NormalFloat", SnacksNormalNC = "NormalFloat", SnacksBorder = "FloatBorder",
    SnacksPickerMatch = "Function", SnacksPickerSelected = "PmenuSel",
    MiniIndentscopeSymbol = "Comment", IblIndent = "NonText", IblScope = "Comment",
  }
  for name, target in pairs(links) do
    groups[name] = { link = target }
  end
  groups.NeoTreeNormal = { fg = p.fg, bg = p.panel }
  groups.NeoTreeNormalNC = { fg = p.fg, bg = p.panel }
  groups.NeoTreeFileName = { fg = p.fg }

  for severity, color in pairs({ Error = p.error, Warn = p.warning, Info = p.info, Hint = p.hint }) do
    groups["Diagnostic" .. severity] = { fg = color }
    groups["DiagnosticSign" .. severity] = { fg = color, bg = p.bg, bold = severity == "Error" }
    groups["DiagnosticFloating" .. severity] = { fg = color, bg = p.float }
    groups["DiagnosticVirtualText" .. severity] = { fg = color, bg = p.bg }
    groups["DiagnosticVirtualLines" .. severity] = { fg = color, bg = p.bg }
    groups["DiagnosticUnderline" .. severity] = { sp = color, undercurl = true }
  end
  groups.DiagnosticOk = { fg = p.focus }
  groups.DiagnosticUnnecessary = { fg = p.comment }
  groups.DiagnosticDeprecated = { fg = p.comment, strikethrough = true }
  for name, color in pairs({ Bad = p.error, Cap = p.type, Local = p.hint, Rare = p.constant }) do
    groups["Spell" .. name] = { sp = color, undercurl = true }
  end

  -- Align semantic tokens with syntax; avoid server-specific color drift.
  for token, target in pairs({
    variable = "@variable", parameter = "@variable.parameter", property = "@property",
    ["function"] = "@function", method = "@function.method", class = "@type",
    interface = "@type", struct = "@type", enum = "@type", type = "@type",
    typeParameter = "@type", namespace = "@module", enumMember = "@constant",
    macro = "@constant.macro", keyword = "@keyword", string = "@string",
    number = "@number", comment = "@comment", operator = "@operator",
    decorator = "@attribute", event = "@type",
  }) do
    groups["@lsp.type." .. token] = { link = target }
  end
  groups["@lsp.mod.readonly"] = { link = "Constant" }
  groups["@lsp.mod.deprecated"] = { strikethrough = true }

  for name, attributes in pairs(groups) do
    vim.api.nvim_set_hl(0, name, attributes)
  end
  for index = 0, 15 do
    vim.g["terminal_color_" .. index] = p.ansi[index]
  end
end

return M
