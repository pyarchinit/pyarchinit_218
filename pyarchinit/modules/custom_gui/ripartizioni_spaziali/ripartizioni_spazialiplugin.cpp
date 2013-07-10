#include "ripartizioni_spaziali.h"
#include "ripartizioni_spazialiplugin.h"

#include <QtPlugin>

ripartizioni_spazialiPlugin::ripartizioni_spazialiPlugin(QObject *parent)
    : QObject(parent)
{
    m_initialized = false;
}

void ripartizioni_spazialiPlugin::initialize(QDesignerFormEditorInterface * /* core */)
{
    if (m_initialized)
        return;
    
    // Add extension registrations, etc. here
    
    m_initialized = true;
}

bool ripartizioni_spazialiPlugin::isInitialized() const
{
    return m_initialized;
}

QWidget *ripartizioni_spazialiPlugin::createWidget(QWidget *parent)
{
    return new ripartizioni_spaziali(parent);
}

QString ripartizioni_spazialiPlugin::name() const
{
    return QLatin1String("ripartizioni_spaziali");
}

QString ripartizioni_spazialiPlugin::group() const
{
    return QLatin1String("");
}

QIcon ripartizioni_spazialiPlugin::icon() const
{
    return QIcon();
}

QString ripartizioni_spazialiPlugin::toolTip() const
{
    return QLatin1String("");
}

QString ripartizioni_spazialiPlugin::whatsThis() const
{
    return QLatin1String("");
}

bool ripartizioni_spazialiPlugin::isContainer() const
{
    return false;
}

QString ripartizioni_spazialiPlugin::domXml() const
{
    return QLatin1String("<widget class=\"ripartizioni_spaziali\" name=\"ripartizioni_spaziali\">\n</widget>\n");
}

QString ripartizioni_spazialiPlugin::includeFile() const
{
    return QLatin1String("ripartizioni_spaziali.h");
}

Q_EXPORT_PLUGIN2(ripartizioni_spazialiplugin, ripartizioni_spazialiPlugin)
