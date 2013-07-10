// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    width: 360
    height: 360
    Text {
        anchors.centerIn: parent
        text: "Hello World"
    }
    MouseArea {
        x: 0
        y: 0
        width: 360
        height: 360
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.fill: parent
        onClicked: {
            Qt.quit();
        }

        Text {
            id: text1
            x: 52
            y: 105
            width: 136
            height: 26
            text: qsTr("text")
            font.pixelSize: 12
        }
    }
}
