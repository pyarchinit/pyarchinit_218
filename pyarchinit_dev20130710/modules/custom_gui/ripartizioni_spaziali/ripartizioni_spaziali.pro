CONFIG      += designer plugin debug_and_release
TARGET      = $$qtLibraryTarget(ripartizioni_spazialiplugin)
TEMPLATE    = lib

HEADERS     = ripartizioni_spazialiplugin.h
SOURCES     = ripartizioni_spazialiplugin.cpp
RESOURCES   = icons.qrc
LIBS        += -L. 

target.path = $$[QT_INSTALL_PLUGINS]/designer
INSTALLS    += target

include(ripartizioni_spaziali.pri)
