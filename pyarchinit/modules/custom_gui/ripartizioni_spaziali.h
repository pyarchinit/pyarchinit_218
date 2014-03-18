#ifndef RIPARTIZIONI_SPAZIALI_H
#define RIPARTIZIONI_SPAZIALI_H

#include <QDialog>

namespace Ui {
class ripartizioni_spaziali;
}

class ripartizioni_spaziali : public QDialog
{
    Q_OBJECT
    
public:
    explicit ripartizioni_spaziali(QWidget *parent = 0);
    ~ripartizioni_spaziali();
    
private:
    Ui::ripartizioni_spaziali *ui;
};

#endif // RIPARTIZIONI_SPAZIALI_H
