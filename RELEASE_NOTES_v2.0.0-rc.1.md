## What's Changed

**🔄 Matugen Migration & Preset Catalogue**
* refactor(themes): regenerate 560 presets from source_color with matugen https://github.com/SakibShahariar/material-gnome-theme/commit/35b36629081b124d9c7c4115a932ec8e594e4c63
* refactor(themes): regenerate 12 remaining hand-crafted families https://github.com/SakibShahariar/material-gnome-theme/commit/cc2b93fbe934f26b52e2312511b98b91c74af825
* Prepare empty theme preset directory for Matugen migration https://github.com/SakibShahariar/material-gnome-theme/commit/d055f3aa0ecf27bb39793ad72da38a4c89003f9b
* feat: render GTK and Shell palettes from JSON presets (#60) https://github.com/SakibShahariar/material-gnome-theme/commit/1941f5be1c66d5c80ee13370dda0796160e26d73
* docs: define shared GTK and Shell color contract (#73) https://github.com/SakibShahariar/material-gnome-theme/commit/051a445ef1e49b658250de53befb2819a26e710a
* docs: add shared Matugen template configuration (#73) https://github.com/SakibShahariar/material-gnome-theme/commit/1d12a18364076505255a23a977bbc3292ed43952

**🎨 Palette Refinements & Contrast**
* refine: balance and diversify accent palettes across families (40 commits) https://github.com/SakibShahariar/material-gnome-theme/commit/a9cd97cdaa95f05ec831493ecac362f8bebcf75a
* fix(themes): correct error hue and text contrast in premade presets https://github.com/SakibShahariar/material-gnome-theme/commit/22f1801d2254b77ed84404e4dc5821cec5d0d895
* fix: align default GTK3 GTK4 and Shell palettes (#59) https://github.com/SakibShahariar/material-gnome-theme/commit/ed2528e19f3f25f331924f94a4723f254b54524c
* chore(theme): sync GTK color outputs with current palette https://github.com/SakibShahariar/material-gnome-theme/commit/bc829485df5a8c3edcf77ddced3c3dbd1d0d69b8
* fix(gtk4): dedupe palette color definitions https://github.com/SakibShahariar/material-gnome-theme/commit/1686b29d7894a4ff98ececaf5f76c5675a4c0c57

**🛠️ GNOME Shell & Top Bar**
* feat(scripts): add set-layout.sh one-command layout switcher (#75) https://github.com/SakibShahariar/material-gnome-theme/commit/36349456a017bc0491973942ff9f823efd0c2b58
* style(gnome-shell): style built-in .tooltip St node to match theme https://github.com/SakibShahariar/material-gnome-theme/commit/f95496002fa3740758b44661520a390a646c09ca
* improved top bar layouts with better hover and active states https://github.com/SakibShahariar/material-gnome-theme/commit/0db8ca3de5b58a5c57f67a14d0825d1d339554be
* fixed overview bg color https://github.com/SakibShahariar/material-gnome-theme/commit/4164d8864da3588c7313e92aa6477e1436db234c
* fixed button flickering issue https://github.com/SakibShahariar/material-gnome-theme/commit/933a22662e2e2317f4c086e544e4938e6fb4585c
* panel, overview and workspace polish across shell styles https://github.com/SakibShahariar/material-gnome-theme/commit/0b527d814457d1961fe4d7a1bb88ce15097f9beb

**🧩 GTK3 / GTK4 Component Fixes**
* fix(gtk4): remove dead menubar rules and use .toolbar class https://github.com/SakibShahariar/material-gnome-theme/commit/e53b5f018896c387c3ac96f23165b3f9f88fd083
* fix(gtk4): make category-play gradient palette-driven https://github.com/SakibShahariar/material-gnome-theme/commit/8ec4b2cf99d26e30ef9d05171abe7b75fd97d061
* fix(gtk4): replace undefined sidebar backdrop color with palette vars https://github.com/SakibShahariar/material-gnome-theme/commit/55a24b19c69b1c19e4a2da6ab04cdbddea0ef036
* fix(gtk4): scope header-popover primary buttons to icon-only https://github.com/SakibShahariar/material-gnome-theme/commit/e936e6da8a64aab7c4cbbff420296460a0e123ce
* fix(gtk4): keep arrow contrast inside hovered/checked buttons https://github.com/SakibShahariar/material-gnome-theme/commit/4eb8502def82d8487b2878a17d55a94bd1fa73aa
* fix: widget-level fixes across rows, sidebar, popovers and nautilus https://github.com/SakibShahariar/material-gnome-theme/commit/9a1317daf9df05f23242103e8d1981af84308ad0
* docs: link GTK4 color definitions during installation (#64) https://github.com/SakibShahariar/material-gnome-theme/commit/40cb9bc34b83d3cc2a446e1fb1f5dafe3b7d602b

**📦 Tooling & Docs**
* feat(scripts): add theme status (#83) and doctor (#84) commands https://github.com/SakibShahariar/material-gnome-theme/commit/944aaf3e4fc5060f8e1b820d96d553a2d96d781b
* feat: add installer and automated theme validation (#67) https://github.com/SakibShahariar/material-gnome-theme/commit/f03034fff0e18b3350a202e58ccfe67ccf788108
* docs: document layout templates and fix shell CSS guidance https://github.com/SakibShahariar/material-gnome-theme/commit/f5feb33f355b6c11c0f9914e21307a2a02849726
* docs: document GTK and GNOME compatibility baseline (#66) https://github.com/SakibShahariar/material-gnome-theme/commit/030ce5c42fbf6e70aea7bd3ea8b74d936a621977
* docs: correct GTK animation reduction instructions (#61) https://github.com/SakibShahariar/material-gnome-theme/commit/fd4b33885cf78daff08183690697738d86988332
* docs: define issue triage categories https://github.com/SakibShahariar/material-gnome-theme/commit/d47a62b693ad95d14dd2e6bdd6b42bca4984ccd1
* docs: add AI agent instructions https://github.com/SakibShahariar/material-gnome-theme/commit/79457a42a1186de89e937e2c6e3598070629e4d2

**Full Changelog**: https://github.com/SakibShahariar/material-gnome-theme/compare/v.1.3.0...v2.0.0-rc.1
