import parcourir
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget,\
    QHBoxLayout,QSpinBox,QDoubleSpinBox,QPushButton,QLabel,QCheckBox, QComboBox, QFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import compare as c

# Exécution de la logique principale
input_files = parcourir.definir_echantillon(sys.argv[1])
distance =  int(sys.argv[2])
id = float(sys.argv[3])

# Affichage des résultats
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pierep_comboxes = {}
        self.infos_layouts = {}
        self.id_spinboxes = {}
        self.distance_spinboxes = {}
        self.pieplot_layouts = {}
        self.histplot_layouts = {}
        self.etatcheck = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Analyse des Variants')
        self.setGeometry(100,100,1250,500)
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Préparation des données pour les plots
        self.data_seq, self.data_noseq = c.compare(input_files, distance, id)
        self.donnees_histogramme = {}
        self.pourcentages = {}
        self.sizeplot = 400
        # Création des onglets pour chaque échantillon
        for echantillon in self.data_seq.keys():
            onglet = QWidget()
            main_layout, hist_layouts, pie_layouts = QVBoxLayout(), QVBoxLayout(), QVBoxLayout()
            tab_layout, spin_layout = QHBoxLayout(), QHBoxLayout()

            # Création de l'interface pour l'histogramme
            check_layout = QVBoxLayout()
            checkbox = QCheckBox(f"Inclure data_noseq pour {echantillon}")
            checkbox.setChecked(True)
            self.etatcheck[echantillon] = True
            checkbox.stateChanged.connect(self.on_check_confirm)
            check_layout.addWidget(checkbox)

            histplot_layout = QVBoxLayout()
            self.donnees_histogramme[echantillon] = self.preparer_donnees_histogramme(self.data_seq[echantillon],self.data_noseq[echantillon])
            histogram_canvas = self.create_hist(echantillon)
            histogram_canvas.setMinimumWidth(self.sizeplot)
            histogram_canvas.setMinimumHeight(self.sizeplot)
            histplot_layout.addWidget(histogram_canvas)
            self.histplot_layouts[echantillon] = histplot_layout

            hist_layouts.addLayout(check_layout)
            hist_layouts.addLayout(histplot_layout)

            # Création de l'interface pour le pieplot
            combo_layout = QVBoxLayout()
            comboBox = QComboBox()
            comboBox.addItems(self.data_seq[echantillon].keys())
            paire_max = max(self.data_seq[echantillon], key=self.data_seq[echantillon].get)
            comboBox.setCurrentIndex(list(self.data_seq[echantillon].keys()).index(paire_max))
            comboBox.currentIndexChanged.connect(self.on_combobox_changed)
            self.pierep_comboxes[echantillon] = comboBox
            combo_layout.addWidget(comboBox)

            pieplot_layout = QHBoxLayout()
            self.pourcentages[echantillon] = self.calculer_pourcentages(self.data_seq[echantillon],self.data_noseq[echantillon])
            pie_canvas = self.create_pieplot(echantillon,paire_max)
            pie_canvas.setMinimumWidth(self.sizeplot)
            pie_canvas.setMinimumHeight(self.sizeplot)
            pieplot_layout.addWidget(pie_canvas)
            self.pieplot_layouts[echantillon] = pieplot_layout

            infos_layout = QVBoxLayout()
            infos = self.create_infos(echantillon, paire_max)
            infos_label = QLabel(infos)
            self.infos_layouts[echantillon] = infos_layout
            infos_layout.addWidget(infos_label)

            pie_layouts.addLayout(combo_layout)
            pie_layouts.addLayout(infos_layout)
            pie_layouts.addLayout(pieplot_layout)

            tab_layout.addLayout(hist_layouts)
            tab_layout.addLayout(pie_layouts)

            # Création des spinbox
            spinLayoutContainer = QFrame()
            spinLayoutContainer.setLayout(spin_layout)
            spinLayoutContainer.setFrameShape(QFrame.StyledPanel)
            spinLayoutContainer.setFrameShadow(QFrame.Raised)
            spinLayoutContainer.setStyleSheet("""
                QFrame {
                    border: 2px solid black;
                    border-radius: 10px;
                }
                
                QFrame > QLabel {
                    border: none;
                    background-color: none;
                    padding: 0;
                }
            """)
            spinLayoutContainer.setMaximumHeight(75)
            spin_layout.addStretch()

            distance_layout = QHBoxLayout()
            distance_label = QLabel("Distance:")
            distance_spinbox = self.create_spinbox((0, 1000000), distance, 10)
            self.distance_spinboxes[echantillon] = distance_spinbox
            distance_layout.addWidget(distance_label)
            distance_layout.addWidget(distance_spinbox)
            spin_layout.addLayout(distance_layout)

            spin_layout.addSpacing(200)
            id_layout = QHBoxLayout()
            id_label = QLabel("ID:")
            id_spinbox = self.create_spinbox((0.0, 1.0), id, 0.05, True)
            self.id_spinboxes[echantillon] = id_spinbox
            id_layout.addWidget(id_label)
            id_layout.addWidget(id_spinbox)
            spin_layout.addLayout(id_layout)
            spin_layout.addSpacing(200)

            confirm_layout = QVBoxLayout()
            confirm_button = QPushButton("Calculer")
            confirm_button.clicked.connect(self.on_button_clicked)
            confirm_layout.addWidget(confirm_button)
            spin_layout.addLayout(confirm_layout)

            spin_layout.addStretch()

            main_layout.addLayout(tab_layout)
            main_layout.addSpacing(50)
            main_layout.addWidget(spinLayoutContainer)
            onglet.setLayout(main_layout)
            self.tab_widget.addTab(onglet, echantillon)
            self.show()

    def on_button_clicked(self):
        current_tab_index = self.tab_widget.currentIndex()
        echantillon = self.tab_widget.tabText(current_tab_index)

        id = self.id_spinboxes[echantillon].value()
        distance = self.distance_spinboxes[echantillon].value()
        input_file = {echantillon: input_files[echantillon]}
        data_seq, data_noseq = c.compare(input_file, distance, id)

        self.data_seq[echantillon] = data_seq[echantillon]
        self.data_noseq[echantillon] = data_noseq[echantillon]

        self.ubdate_pie(echantillon)
        self.update_hist(echantillon,self.etatcheck[echantillon])

    def on_combobox_changed(self):
        current_tab_index = self.tab_widget.currentIndex()
        current_tab_name = self.tab_widget.tabText(current_tab_index)
        self.ubdate_pie(current_tab_name)

    def on_check_confirm(self,state):
        current_tab_index = self.tab_widget.currentIndex()
        echantillon = self.tab_widget.tabText(current_tab_index)
        self.etat = True
        if state == 0:
            self.etat = False

        self.etatcheck[echantillon] = self.etat
        self.update_hist(echantillon,self.etatcheck[echantillon])

    def update_hist(self, echantillon,noseq):
        self.donnees_histogramme[echantillon] = self.preparer_donnees_histogramme(self.data_seq[echantillon],self.data_noseq[echantillon],noseq)
        self.clear_layout(self.histplot_layouts[echantillon])
        new_hist = self.create_hist(echantillon)
        new_hist.setMinimumWidth(self.sizeplot)
        new_hist.setMinimumHeight(self.sizeplot)
        self.histplot_layouts[echantillon].addWidget(new_hist)

    def ubdate_pie(self,echantillon):
        self.pourcentages[echantillon] = self.calculer_pourcentages(self.data_seq[echantillon],self.data_noseq[echantillon])
        paire = self.pierep_comboxes[echantillon].currentText()

        new_pie = self.create_pieplot(echantillon, paire)
        new_pie.setMinimumWidth(self.sizeplot)
        new_pie.setMinimumHeight(self.sizeplot)
        self.clear_layout(self.pieplot_layouts[echantillon])
        self.pieplot_layouts[echantillon].addWidget(new_pie)

        new_infos = self.create_infos(echantillon, paire)
        new_infosLabel = QLabel(new_infos)
        self.clear_layout(self.infos_layouts[echantillon])
        self.infos_layouts[echantillon].addWidget(new_infosLabel)

    def create_hist(self,echantillon):
        hist = FigureCanvas(plt.Figure(figsize=(200, 200)))

        ax_histogram = hist.figure.subplots()
        ax_histogram.bar(self.donnees_histogramme[echantillon].keys(), self.donnees_histogramme[echantillon].values(),zorder=3)

        max_y = max(self.data_seq[echantillon].values()) + max(
            [sum(i.values()) for i in self.data_noseq[echantillon].values()]) + 10
        ax_histogram.set_ylim([0, max_y])

        for y in range(0, int(max_y), 5):  # Ajoute une ligne horizontale tous les 2 unités
            ax_histogram.axhline(y, color='gray', linestyle='--', linewidth=0.5, zorder=2)

        ax_histogram.set_title(f"Nombre de variants communs entre paire de réplicats",pad=20,fontsize='medium')
        ax_histogram.set_xlabel(f"Paire de réplicats")
        ax_histogram.set_ylabel(f"Nombre de variants communs")

        return hist

    def create_pieplot(self,echantillon,paire):
        data = self.pourcentages[echantillon][paire]
        pie = FigureCanvas(plt.Figure(figsize=(200, 200)))
        ax_pie = pie.figure.subplots()
        ax_pie.pie(data.values(), labels=data.keys(), autopct='%1.1f%%',
                   startangle=140)

        ax_pie.set_title(f"Répartition des types de variants communs entre les réplicats {paire.split('_')[0]} et {paire.split('_')[1]}",fontsize='medium')
        return pie

    def preparer_donnees_histogramme(self, data_seq, data_noseq, noseq=True):
        donnees_histogramme = {}
        for comp in data_seq:
            donnees_histogramme[comp] = {}
            total = data_seq[comp]
            if noseq:
                if comp in data_noseq:
                    total += sum(data_noseq[comp].values())
            donnees_histogramme[comp] = total
        return donnees_histogramme

    def calculer_pourcentages(self, data_seq, data_noseq):
        resultats = {}
        for comp in data_seq:
            resultats[comp] = {}
            total = data_seq[comp]
            types_noseq = data_noseq.get(comp, {})
            for type_noseq, nombre in types_noseq.items():
                total += nombre
            if total != 0:
                resultats[comp]['séquence(s)'] = (data_seq[comp] / total) * 100
            for type_noseq, nombre in types_noseq.items():
                if total != 0:
                    resultats[comp][type_noseq] = (nombre / total) * 100
        return resultats

    def create_infos(self,echantillon,paire):
        seq = self.data_seq[echantillon][paire]
        type_noseq = self.data_noseq[echantillon][paire]
        noseqs_string = ""
        total_noseq = 0

        for noseq in type_noseq:
            noseq_string = f"{self.data_noseq[echantillon][paire][noseq]} {noseq}"
            noseqs_string += f"; {noseq_string}"
            total_noseq += int(self.data_noseq[echantillon][paire][noseq])

        return f"Nombre de variant commun entre {paire.split('_')[0]} et {paire.split('_')[1]} =  {int(seq) + total_noseq}  ( {seq} séquence(s) {noseqs_string}) "

    def create_spinbox(self, range, value, step, float = False,decimal=2):
        if float:
            spinbox = QDoubleSpinBox()
            spinbox.setDecimals(decimal)
        else:
            spinbox = QSpinBox()

        spinbox.setRange(range[0],range[1])
        spinbox.setValue(value)
        spinbox.setSingleStep(step)
        return spinbox

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stylesheet = """
        QWidget {
            font-family: 'Roboto'; /*  police */
            font-size: 10pt;
            color: #575757; /*  couleur de police*/
            background-color: #ffffff; /* Fond blanc */
        }
        QCheckBox {
            padding: 5px;
            spacing: 5px; /* Ajoutez de l'espace autour du texte de la case à cocher */
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        QPushButton {
            background-color:rgba(27, 217, 8, 0.34); 
            font-weight: bold; /* Rendre le texte du bouton en gras */
            border-radius: 10px; /* Coins arrondis */
            padding: 10px;
            border: none;
            text-transform: uppercase; /* Texte en majuscules */
        }
        QPushButton:hover {
            background-color:rgba(226, 86, 118, 1); /* plus clair pour l'effet de survol */
        }
        QComboBox {
            border: 2px solid #C4C4C3; /* Bordure */
            border-radius: 10px;
            padding: 5px 10px; /* Padding horizontal plus grand */
            min-width: 6em;
            selection-background-color: #D3D3D3; /* Couleur de fond pour l'élément sélectionné */
            color: grey;
        }
        QComboBox:hover {
            background-color: rgba(0, 115, 255, 0.34);  /* Couleur de fond au survol */
        }
        QComboBox QAbstractItemView {
            color: black;  /* Couleur du texte pour les éléments de la liste */
        }
        QLabel {
            qproperty-alignment: 'AlignLeft | AlignVCenter';
            padding: 2px;
            margin: 0 5px; /* Ajouter une marge horizontale pour le label */
        }
        /* Ajouter des styles */
        QTabWidget::pane {
            border-top: 2px solid #C4C4C3; /* Bordure en haut */
        }
        QTabBar::tab {
            background: #E1E1E1;
            border: 1px solid #C4C4C3;
            border-bottom: none; /* Pas de bordure en bas pour fondre avec le panneau */
            border-top-left-radius: 4px; /* Arrondir les coins supérieurs */
            border-top-right-radius: 4px;
            padding: 5px 10px; /* Plus d'espace horizontal pour les onglets */
            margin-right: 2px; /* Ajouter un peu d'espace entre les onglets */
            min-width: 50px;
            max-height: 15px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: #ffffff; /* Fond blanc pour l'onglet sélectionné ou survolé */
            font-weight: bold; /* Texte en gras pour l'onglet sélectionné ou survolé */
        }
    """

    app.setStyleSheet(stylesheet)
    ex = App()
    sys.exit(app.exec_())
