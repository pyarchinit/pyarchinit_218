#include "ripartizioni_spaziali.h"
#include "ui_ripartizioni_spaziali.h"

ripartizioni_spaziali::ripartizioni_spaziali(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::ripartizioni_spaziali)
{
    ui->setupUi(this);
}

ripartizioni_spaziali::~ripartizioni_spaziali()
{
    delete ui;
}
