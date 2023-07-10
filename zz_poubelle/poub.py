self.xmlParam = {
          "parameters": {
            "networkName": self.nomReseau.text(),
            "computationOptions": {
              "networkType": str(self.typeCalcul.currentText()),
              "calculationDimension": str(self.dimensionCalcul.currentText()),
              "maxIterationNbr": str(self.nbIterationsMax.value()),
              "interruptionCondition": str(self.critereIterruption.value()),
              "robust": self.isCheckedString(self.robuste),
              "robustLimit": str(self.cRobuste.value()),
              "refractionk": str(round(self.refractionk.value(),3)),
              "sigmaRefractionk": str(self.sigmarefraction.value())
            },
            "groups": {
              "distanceGroups": {
                "distanceGroup": self.listeGroupesDistance
              },
              "directionGroups": {
                "directionGroup": self.listeGroupesDirection
              },
              "gnssGroups": {
                "gnssGroup": self.listeGroupesGnss
              },
              "centringGroups": {
                "centringGroup": self.listeGroupesCentrage
              },
              "localSystemGroups": {
                "localSystemGroup": self.listeGroupesSystemeLocal
              },
              "simpleMeasureGroups": {
                "simpleMeasureGroup": self.listeGroupesCote
              }
            },
            "planimetricControlPoints": {
              "point": self.listePFplani
            },
            "altimetricControlPoints": {
              "point": self.listePFalti
            }
          }
        }