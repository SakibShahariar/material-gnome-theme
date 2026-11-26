# GTK3 CSS node reference

Reference extracted from the official GTK 3 documentation
(https://docs.gtk.org/gtk3/) for the widget-by-widget stylesheet review.
Each section below is the "CSS nodes" heading of the corresponding widget
class page. This is a lookup table for maintainers; it is not generated into
the stylesheet and does not affect rendering.

Source: https://docs.gtk.org/gtk3/

## class.AccelLabel.html

label
╰── accelerator
Like GtkLabel, GtkAccelLabel has a main CSS node with the name label.
It adds a subnode with name accelerator.

## class.ActionBar.html

GtkActionBar has a single CSS node with name actionbar.

## class.AppChooserWidget.html

GtkAppChooserWidget has a single CSS node with name appchooser.

## class.AspectFrame.html

GtkAspectFrame uses a CSS node with name frame.

## class.Assistant.html

GtkAssistant has a single CSS node with the name assistant.

## class.Box.html

GtkBox uses a single CSS node with name box.
In horizontal orientation, the nodes of the children are always arranged
from left to right. So :first-child will always select the leftmost child,
regardless of text direction.

## class.Button.html

GtkButton has a single CSS node with name button. The node will get the
style classes .image-button or .text-button, if the content is just an
image or label, respectively. It may also receive the .flat style class.
Other style classes that are commonly used with GtkButton include
.suggested-action and .destructive-action. In special cases, buttons
can be made round by adding the .circular style class.
Button-like widgets like GtkToggleButton, GtkMenuButton, GtkVolumeButton,
GtkLockButton, GtkColorButton, GtkFontButton or GtkFileChooserButton use
style classes such as .toggle, .popup, .scale, .lock, .color, .font, .file
to differentiate themselves from a plain GtkButton.

## class.CellView.html

GtkCellView has a single CSS node with name cellview.

## class.CheckButton.html

checkbutton
├── check
╰── <child>
A GtkCheckButton with indicator (see gtk_toggle_button_set_mode()) has a
main CSS node with name checkbutton and a subnode with name check.
button.check
├── check
╰── <child>
A GtkCheckButton without indicator changes the name of its main node
to button and adds a .check style class to it. The subnode is invisible
in this case.

## class.CheckMenuItem.html

menuitem
├── check.left
╰── <child>
GtkCheckMenuItem has a main CSS node with name menuitem, and a subnode
with name check, which gets the .left or .right style class.

## class.ColorButton.html

GtkColorButton has a single CSS node with name button. To differentiate
it from a plain GtkButton, it gets the .color style class.

## class.ComboBox.html

combobox
├── box.linked
│   ╰── button.combo
│       ╰── box
│           ├── cellview
│           ╰── arrow
╰── window.popup
A normal combobox contains a box with the .linked class, a button
with the .combo class and inside those buttons, there are a cellview and
an arrow.
combobox
├── box.linked
│   ├── entry.combo
│   ╰── button.combo
│       ╰── box
│           ╰── arrow
╰── window.popup
A GtkComboBox with an entry has a single CSS node with name combobox. It
contains a box with the .linked class. That box contains an entry and a
button, both with the .combo class added.
The button also contains another node with name arrow.

## class.ComboBoxText.html

combobox
╰── box.linked
├── entry.combo
├── button.combo
╰── window.popup
GtkComboBoxText has a single CSS node with name combobox. It adds
the style class .combo to the main CSS nodes of its entry and button
children, and the .linked class to the node of its internal box.

## class.Entry.html

entry[.read-only][.flat][.warning][.error]
├── image.left
├── image.right
├── undershoot.left
├── undershoot.right
├── [selection]
├── [progress[.pulse]]
╰── [window.popup]
GtkEntry has a main node with the name entry. Depending on the properties
of the entry, the style classes .read-only and .flat may appear. The style
classes .warning and .error may also be used with entries.
When the entry shows icons, it adds subnodes with the name image and the
style class .left or .right, depending on where the icon appears.
When the entry has a selection, it adds a subnode with the name selection.
When the entry shows progress, it adds a subnode with the name progress.
The node has the style class .pulse when the shown progress is pulsing.
The CSS node for a context menu is added as a subnode below entry as well.
The undershoot nodes are used to draw the underflow indication when content
is scrolled out of view. These nodes get the .left and .right style classes
added depending on where the indication is drawn.
When touch is used and touch selection handles are shown, they are using
CSS nodes with name cursor-handle. They get the .top or .bottom style class
depending on where they are shown in relation to the selection. If there is
just a single handle for the text cursor, it gets the style class .insertion-cursor.

## class.Expander.html

expander
├── title
│   ├── arrow
│   ╰── <label widget>
╰── <child>
GtkExpander has three CSS nodes, the main node with the name expander,
a subnode with name title and node below it with name arrow. The arrow of an
expander that is showing its child gets the :checked pseudoclass added to it.

## class.FileChooserButton.html

GtkFileChooserButton has a CSS node with name “filechooserbutton”, containing
a subnode for the internal button with name “button” and style class “.file”.

## class.FileChooserWidget.html

GtkFileChooserWidget has a single CSS node with name filechooser.

## class.FlowBox.html

flowbox
├── flowboxchild
│   ╰── <child>
├── flowboxchild
│   ╰── <child>
┊
╰── [rubberband]
GtkFlowBox uses a single CSS node with name flowbox. GtkFlowBoxChild
uses a single CSS node with name flowboxchild.
For rubberband selection, a subnode with name rubberband is used.

## class.FontButton.html

GtkFontButton has a single CSS node with name button and style class .font.

## class.FontChooserWidget.html

GtkFontChooserWidget has a single CSS node with name fontchooser.

## class.Frame.html

frame
├── border[.flat]
├── <label widget>
╰── <child>
GtkFrame has a main CSS node named “frame” and a subnode named “border”. The
“border” node is used to draw the visible border. You can set the appearance
of the border using CSS properties like “border-style” on the “border” node.
The border node can be given the style class “.flat”, which is used by themes
to disable drawing of the border. To do this from code, call
gtk_frame_set_shadow_type() with GTK_SHADOW_NONE to add the “.flat” class or
any other shadow type to remove it.

## class.Grid.html

GtkGrid uses a single CSS node with name grid.

## class.IconView.html

iconview.view
╰── [rubberband]
GtkIconView has a single CSS node with name iconview and style class .view.
For rubberband selection, a subnode with name rubberband is used.

## class.Image.html

GtkImage has a single CSS node with the name image. The style classes
may appear on image CSS nodes: .icon-dropshadow, .lowres-icon.

## class.InfoBar.html

GtkInfoBar has a single CSS node with name infobar. The node may get
one of the style classes .info, .warning, .error or .question, depending
on the message type.

## class.Label.html

label
├── [selection]
├── [link]
┊
╰── [link]
GtkLabel has a single CSS node with the name label. A wide variety
of style classes may be applied to labels, such as .title, .subtitle,
.dim-label, etc. In the GtkShortcutsWindow, labels are used wth the
.keycap style class.
If the label has a selection, it gets a subnode with name selection.
If the label has links, there is one subnode per link. These subnodes
carry the link or visited state depending on whether they have been visited.

## class.LevelBar.html

levelbar[.discrete]
╰── trough
├── block.filled.level-name
┊
├── block.empty
┊
GtkLevelBar has a main CSS node with name levelbar and one of the style
classes .discrete or .continuous and a subnode with name trough. Below the
trough node are a number of nodes with name block and style class .filled
or .empty. In continuous mode, there is exactly one node of each, in discrete
mode, the number of filled and unfilled nodes corresponds to blocks that are
drawn. The block.filled nodes also get a style class .level-name corresponding
to the level for the current value.
In horizontal orientation, the nodes are always arranged from left to right,
regardless of text direction.

## class.LinkButton.html

GtkLinkButton has a single CSS node with name button. To differentiate
it from a plain GtkButton, it gets the .link style class.

## class.ListBox.html

list
╰── row[.activatable]
GtkListBox uses a single CSS node named list. Each GtkListBoxRow uses
a single CSS node named row. The row nodes get the .activatable
style class added when appropriate.

## class.Menu.html

menu
├── arrow.top
├── <child>
┊
├── <child>
╰── arrow.bottom
The main CSS node of GtkMenu has name menu, and there are two subnodes
with name arrow, for scrolling menu arrows. These subnodes get the
.top and .bottom style classes.

## class.MenuBar.html

GtkMenuBar has a single CSS node with name menubar.

## class.MenuButton.html

GtkMenuButton has a single CSS node with name button. To differentiate
it from a plain GtkButton, it gets the .popup style class.

## class.MenuItem.html

menuitem
├── <child>
╰── [arrow.right]
GtkMenuItem has a single CSS node with name menuitem. If the menuitem
has a submenu, it gets another CSS node with name arrow, which has
the .left or .right style class.

## class.ModelButton.html

modelbutton
├── <child>
╰── check
modelbutton
├── <child>
╰── radio
modelbutton
├── <child>
╰── arrow
GtkModelButton has a main CSS node with name modelbutton, and a subnode,
which will have the name check, radio or arrow, depending on the role
of the button and whether it has a menu name set.
The subnode is positioned before or after the content nodes and gets the
.left or .right style class, depending on where it is located.
button.model
├── <child>
╰── check
Iconic model buttons (see GtkModelButton:iconic) change the name of
their main node to button and add a .model style class to it. The indicator
subnode is invisible in this case.

## class.Notebook.html

notebook
├── header.top
│   ├── [<action widget>]
│   ├── tabs
│   │   ├── [arrow]
│   │   ├── tab
│   │   │   ╰── <tab label>
┊   ┊   ┊
│   │   ├── tab[.reorderable-page]
│   │   │   ╰── <tab label>
│   │   ╰── [arrow]
│   ╰── [<action widget>]
│
╰── stack
├── <child>
┊
╰── <child>
GtkNotebook has a main CSS node with name notebook, a subnode
with name header and below that a subnode with name tabs which
contains one subnode per tab with name tab.
If action widgets are present, their CSS nodes are placed next
to the tabs node. If the notebook is scrollable, CSS nodes with
name arrow are placed as first and last child of the tabs node.
The main node gets the .frame style class when the notebook
has a border (see gtk_notebook_set_show_border()).
The header node gets one of the style class .top, .bottom,
.left or .right, depending on where the tabs are placed. For
reorderable pages, the tab node gets the .reorderable-page class.
A tab node gets the .dnd style class while it is moved with drag-and-drop.
The nodes are always arranged from left-to-right, regarldess of text direction.

## class.Overlay.html

GtkOverlay has a single CSS node with the name “overlay”. Overlay children
whose alignments cause them to be positioned at an edge get the style classes
“.left”, “.right”, “.top”, and/or “.bottom” according to their position.

## class.Paned.html

paned
├── <child>
├── separator[.wide]
╰── <child>
GtkPaned has a main CSS node with name paned, and a subnode for
the separator with name separator. The subnode gets a .wide style
class when the paned is supposed to be wide.
In horizontal orientation, the nodes of the children are always arranged
from left to right. So :first-child will always select the leftmost child,
regardless of text direction.

## class.PlacesSidebar.html

GtkPlacesSidebar uses a single CSS node with name placessidebar and style
class .sidebar.
Among the children of the places sidebar, the following style classes can
be used:
- .sidebar-new-bookmark-row for the ‘Add new bookmark’ row
- .sidebar-placeholder-row for a row that is a placeholder
- .has-open-popup when a popup is open for a row.

## class.Popover.html

GtkPopover has a single css node called popover. It always gets the
.background style class and it gets the .menu style class if it is
menu-like (e.g. GtkPopoverMenu or created using gtk_popover_new_from_model().
Particular uses of GtkPopover, such as touch selection popups
or magnifiers in GtkEntry or GtkTextView get style classes
like .touch-selection or .magnifier to differentiate from
plain popovers.

## class.ProgressBar.html

progressbar[.osd]
├── [text]
╰── trough[.empty][.full]
╰── progress[.pulse]
GtkProgressBar has a main CSS node with name progressbar and subnodes with
names text and trough, of which the latter has a subnode named progress. The
text subnode is only present if text is shown. The progress subnode has the
style class .pulse when in activity mode. It gets the style classes .left,
.right, .top or .bottom added when the progress ‘touches’ the corresponding
end of the GtkProgressBar. The .osd class on the progressbar node is for use
in overlays like the one Epiphany has for page loading progress.

## class.RadioButton.html

radiobutton
├── radio
╰── <child>
A GtkRadioButton with indicator (see gtk_toggle_button_set_mode()) has a
main CSS node with name radiobutton and a subnode with name radio.
button.radio
├── radio
╰── <child>
A GtkRadioButton without indicator changes the name of its main node
to button and adds a .radio style class to it. The subnode is invisible
in this case.

## class.RadioMenuItem.html

menuitem
├── radio.left
╰── <child>
GtkRadioMenuItem has a main CSS node with name menuitem, and a subnode
with name radio, which gets the .left or .right style class.

## class.RadioToolButton.html

GtkRadioToolButton has a single CSS node with name toolbutton.

## class.Revealer.html

GtkRevealer has a single CSS node with name revealer.
The GtkRevealer widget was added in GTK+ 3.10.

## class.Scale.html

scale[.fine-tune][.marks-before][.marks-after]
├── marks.top
│   ├── mark
│   ┊    ├── [label]
│   ┊    ╰── indicator
┊   ┊
│   ╰── mark
├── [value]
├── contents
│   ╰── trough
│       ├── slider
│       ├── [highlight]
│       ╰── [fill]
╰── marks.bottom
├── mark
┊    ├── indicator
┊    ╰── [label]
╰── mark
GtkScale has a main CSS node with name scale and a subnode for its contents,
with subnodes named trough and slider.
The main node gets the style class .fine-tune added when the scale is in
‘fine-tuning’ mode.
If the scale has an origin (see gtk_scale_set_has_origin()), there is a
subnode with name highlight below the trough node that is used for rendering
the highlighted part of the trough.
If the scale is showing a fill level (see gtk_range_set_show_fill_level()),
there is a subnode with name fill below the trough node that is used for
rendering the filled in part of the trough.
If marks are present, there is a marks subnode before or after the contents
node, below which each mark gets a node with name mark. The marks nodes get
either the .top or .bottom style class.
The mark node has a subnode named indicator. If the mark has text, it also
has a subnode named label. When the mark is either above or left of the
scale, the label subnode is the first when present. Otherwise, the indicator
subnode is the first.
The main CSS node gets the ‘marks-before’ and/or ‘marks-after’ style classes
added depending on what marks are present.
If the scale is displaying the value (see GtkScale:draw-value), there is
subnode with name value.

## class.ScaleButton.html

GtkScaleButton has a single CSS node with name button. To differentiate
it from a plain GtkButton, it gets the .scale style class.
The popup widget that contains the scale has a .scale-popup style class.

## class.Scrollbar.html

scrollbar[.fine-tune]
╰── contents
├── [button.up]
├── [button.down]
├── trough
│   ╰── slider
├── [button.up]
╰── [button.down]
GtkScrollbar has a main CSS node with name scrollbar and a subnode for its
contents, with subnodes named trough and slider.
The main node gets the style class .fine-tune added when the scrollbar is
in ‘fine-tuning’ mode.
If steppers are enabled, they are represented by up to four additional
subnodes with name button. These get the style classes .up and .down to
indicate in which direction they are moving.
Other style classes that may be added to scrollbars inside GtkScrolledWindow
include the positional classes (.left, .right, .top, .bottom) and style
classes related to overlay scrolling (.overlay-indicator, .dragging, .hovering).

## class.ScrolledWindow.html

GtkScrolledWindow has a main CSS node with name scrolledwindow.
It uses subnodes with names overshoot and undershoot to
draw the overflow and underflow indications. These nodes get
the .left, .right, .top or .bottom style class added depending
on where the indication is drawn.
GtkScrolledWindow also sets the positional style classes (.left,
.right, .top, .bottom) and style classes related to overlay
scrolling (.overlay-indicator, .dragging, .hovering) on its scrollbars.
If both scrollbars are visible, the area where they meet is drawn
with a subnode named junction.

## class.SearchBar.html

GtkSearchBar has a single CSS node with name searchbar.

## class.Separator.html

GtkSeparator has a single CSS node with name separator. The node
gets one of the .horizontal or .vertical style classes.

## class.SeparatorMenuItem.html

GtkSeparatorMenuItem has a single CSS node with name separator.

## class.SeparatorToolItem.html

GtkSeparatorToolItem has a single CSS node with name separator.

## class.SpinButton.html

spinbutton.horizontal
├── undershoot.left
├── undershoot.right
├── entry
│   ╰── ...
├── button.down
╰── button.up
spinbutton.vertical
├── undershoot.left
├── undershoot.right
├── button.up
├── entry
│   ╰── ...
╰── button.down
GtkSpinButtons main CSS node has the name spinbutton. It creates subnodes
for the entry and the two buttons, with these names. The button nodes have
the style classes .up and .down. The GtkEntry subnodes (if present) are put
below the entry node. The orientation of the spin button is reflected in
the .vertical or .horizontal style class on the main node.

## class.Spinner.html

GtkSpinner has a single CSS node with the name spinner. When the animation is
active, the :checked pseudoclass is added to this node.

## class.Stack.html

GtkStack has a single CSS node named stack.

## class.StackSidebar.html

GtkStackSidebar has a single CSS node with name stacksidebar and
style class .sidebar.
When circumstances require it, GtkStackSidebar adds the
.needs-attention style class to the widgets representing the stack pages.

## class.StackSwitcher.html

GtkStackSwitcher has a single CSS node named stackswitcher and
style class .stack-switcher.
When circumstances require it, GtkStackSwitcher adds the
.needs-attention style class to the widgets representing the
stack pages.

## class.Switch.html

switch
╰── slider
GtkSwitch has two css nodes, the main node with the name switch and a subnode
named slider. Neither of them is using any style classes.

## class.TextView.html

textview.view
├── border.top
├── border.left
├── text
│   ╰── [selection]
├── border.right
├── border.bottom
╰── [window.popup]
GtkTextView has a main css node with name textview and style class .view,
and subnodes for each of the border windows, and the main text area,
with names border and text, respectively. The border nodes each get
one of the style classes .left, .right, .top or .bottom.
A node representing the selection will appear below the text node.
If a context menu is opened, the window node will appear as a subnode
of the main node.

## class.ToggleButton.html

GtkToggleButton has a single CSS node with name button. To differentiate
it from a plain GtkButton, it gets the .toggle style class.

## class.ToggleToolButton.html

GtkToggleToolButton has a single CSS node with name togglebutton.

## class.ToolButton.html

GtkToolButton has a single CSS node with name toolbutton.

## class.ToolItemGroup.html

GtkToolItemGroup has a single CSS node named toolitemgroup.

## class.ToolPalette.html

GtkToolPalette has a single CSS node named toolpalette.

## class.Toolbar.html

GtkToolbar has a single CSS node with name toolbar.

## class.TreeView.html

treeview.view
├── header
│   ├── <column header>
┊   ┊
│   ╰── <column header>
│
╰── [rubberband]
GtkTreeView has a main CSS node with name treeview and style class .view.
It has a subnode with name header, which is the parent for all the column
header widgets’ CSS nodes.
For rubberband selection, a subnode with name rubberband is used.

## class.Viewport.html

GtkViewport has a single CSS node with name viewport.

## class.Window.html

window.background
├── decoration
├── <titlebar child>.titlebar [.default-decoration]
╰── <child>
GtkWindow has a main CSS node with name window and style class .background,
and a subnode with name decoration.
Style classes that are typically used with the main CSS node are .csd (when
client-side decorations are in use), .solid-csd (for client-side decorations
without invisible borders), .ssd (used by mutter when rendering server-side
decorations). GtkWindow also represents window states with the following
style classes on the main node: .tiled, .maximized, .fullscreen. Specialized
types of window often add their own discriminating style classes, such as
.popup or .tooltip.
GtkWindow adds the .titlebar and .default-decoration style classes to the
widget that is added as a titlebar child.
