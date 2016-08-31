styleTemplate = """
QWidget
{
	color: %(COLOR_TEXT)s;
	background: %(COLOR_BACKGROUND)s;
}

QLabel
{
	color: white;
	background-color: transparent;
}


QProgressBar
{
	background: rgb(96, 96, 96);
	border: 0px solid black;
}

QListWidget
{
	color: black;
	background: %(COLOR_LIST)s;
	border: 1px solid %(COLOR_BORDER)s;
}


QPlainTextEdit
{
	color: white;
	background: black;
}


QScrollBar:vertical{	width: 10px;	}
QScrollBar:horizontal{	height: 10px;	}

QScrollBar::handle:vertical
{
	background: %(COLOR_BACKGROUND)s;
	border-width: 1px;
	border-color: %(COLOR_BORDER)s;
	border-style: solid;

	border-right-width: 0px;
	margin-top: -1px;
	margin-bottom: -1px;
}

QScrollBar::handle:horizontal
{
	background: %(COLOR_BACKGROUND)s;
	border-width: 1px;
	border-color: %(COLOR_BORDER)s;
	border-style: solid;

	border-bottom-width: 0px;
	margin-left: -1px;
	margin-right: -1px;
}


QScrollBar::add-page, QScrollBar::sub-page
{
	background: %(COLOR_LIST)s;
}


QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{}
QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal{}
"""


colors = {}
colors["COLOR_HOVER"]				= '#953636'
colors["COLOR_ERROR_EMPTYLIST"]		= '#cc4747'
colors["COLOR_BACKGROUND"]			= '#444444'
colors["COLOR_SELECTION"]			= '#953636'
colors["COLOR_TEXT"]				= '#c8c8c8'
colors["COLOR_TEXT_GREY"]			= '#787878'
colors["COLOR_BORDER"]				= '#272727'
colors["COLOR_LIST"]				= '#333333'

STYLE = styleTemplate % colors