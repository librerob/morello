# Design notes

The central relationship is cherry ink against celadon and apricot. The background carries the identity. It stays red-violet through raised surfaces, while sidebars and status lines use a darker shade of the same ground.

The three primary accents have separate jobs. Apricot marks keywords and control flow. Celadon marks functions and the active UI. Citrine marks strings. Blue-grey types and rose constants provide secondary distinctions. Plain variables remain off-white; punctuation uses a more neutral grey above the comment lightness, while staying below the body text. Both are tested as readable text.

The off-white is slightly pink rather than yellow or blue. That makes a large paragraph feel related to the cherry surface without tinting it as strongly as the accent colors. Comments use a muted mauve with a minimum 4.5:1 contrast on all four reading surfaces. Error text shifts toward raspberry to separate it from apricot keywords. Error signs are bold, while diagnostic underlines and severity labels supply cues beyond color.

The main accents do not have identical lightness: functions and strings sit a little above the apricot keywords. This gives declarations and values some prominence without turning keywords into decoration. Diff backgrounds and selected text have their own tested pairs. Search uses a strong fill only while searching.

## Light

The light variant uses blush paper and cherry ink. Its ground has less pink chroma than the first proposal so that large empty areas stay quiet. Raised documentation panels move toward white; sidebars use a slightly deeper blush.

The role relationships remain the same, but the accents are not inverted. Apricot becomes a restrained terracotta, celadon becomes jade, and citrine becomes a dry olive. The terracotta is darker than the green accents to help preserve a distinction when hue differences are reduced. Types stay blue and constants stay rose. These choices were compared in Lua, Python, and TypeScript previews; color-vision simulations are approximate design aids, not a certification or a substitute for user testing.

Every core text role is checked against all nine light surfaces, including selection and diff fills. The dark variant instead supplies an explicit foreground for built-in selection and diff highlights. Light ANSI white and bright white remain pale utility slots; they are unsuitable as text on the light ground. Bright ANSI colors otherwise stay dark enough to read, rather than simply adding luminance.

