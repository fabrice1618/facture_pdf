import time
import glob
import os
import json
import tarfile
import shutil

# configurations
input_dir = '/root/files/input/'
batch_dir = '/root/batch'
archive_dir = '/root/batch/archive/'
doc_dir = '/root/files/documents/'

# deplacer un fichier dans l'archive tar gz
def move_to_tar(fichier, fichier_tar):
    fichier_tar.add(fichier, arcname=fichier)
    os.remove(fichier)

# lecture fichier JSON
def lecture_json(fichier):
    data = {}
    with open(fichier, 'r') as fp:
        data = json.load(fp)

    return data

# creer contenu latex de la facture
def creer_facture_tex( data ):

    template = r"""
\documentclass[a4paper]{article}
\usepackage{import}
\usepackage{template/facture_preambule}
\import{template/}{*!ae_config*!}
\title{facture *!facturenum*!}
\author{\aenom}
\date{*!facturedate*!}
\hypersetup{
pdftitle={Facture *!facturenum*!},
pdfsubject={Facture *!facturenum*!},
pdfauthor={\aenom},
pdfkeywords={\aenom facture *!facturenum*! *!facturedate*!}
}
\xdef\clientnom {*!clientnom*!}
\xdef\clientadresse{*!clientadresse*!}
\xdef\clientville{*!clientville*!}
\xdef\clientpays{*!clientpays*!}
\xdef\facturenum{*!facturenum*!}
\xdef\facturedate{*!facturedate*!}
\xdef\factureobjet{*!factureobjet*!}
\xdef\facturetotal{*!facturetotal*!}
\xdef\adesign{*!adesign*!}
\xdef\adesignbis{*!adesignbis*!}
\xdef\aqte{*!aqte*!}
\xdef\apu{*!apu*!}
\xdef\atotal{*!atotal*!}
\xdef\bdesign{*!bdesign*!}
\xdef\bdesignbis{*!bdesignbis*!}
\xdef\bqte{*!bqte*!}
\xdef\bpu{*!bpu*!}
\xdef\btotal{*!btotal*!}
\xdef\cdesign{*!cdesign*!}
\xdef\cdesignbis{*!cdesignbis*!}
\xdef\cqte{*!cqte*!}
\xdef\cpu{*!cpu*!}
\xdef\ctotal{*!ctotal*!}
\xdef\ddesign{*!ddesign*!}
\xdef\ddesignbis{*!ddesignbis*!}
\xdef\dqte{*!dqte*!}
\xdef\dpu{*!dpu*!}
\xdef\dtotal{*!dtotal*!}
\xdef\edesign{*!edesign*!}
\xdef\edesignbis{*!edesignbis*!}
\xdef\eqte{*!eqte*!}
\xdef\epu{*!epu*!}
\xdef\etotal{*!etotal*!}
\xdef\fdesign{*!fdesign*!}
\xdef\fdesignbis{*!fdesignbis*!}
\xdef\fqte{*!fqte*!}
\xdef\fpu{*!fpu*!}
\xdef\ftotal{*!ftotal*!}
\xdef\gdesign{*!gdesign*!}
\xdef\gdesignbis{*!gdesignbis*!}
\xdef\gqte{*!gqte*!}
\xdef\gpu{*!gpu*!}
\xdef\gtotal{*!gtotal*!}
\xdef\hdesign{*!hdesign*!}
\xdef\hdesignbis{*!hdesignbis*!}
\xdef\hqte{*!hqte*!}
\xdef\hpu{*!hpu*!}
\xdef\htotal{*!htotal*!}
\xdef\idesign{*!idesign*!}
\xdef\idesignbis{*!idesignbis*!}
\xdef\iqte{*!iqte*!}
\xdef\ipu{*!ipu*!}
\xdef\itotal{*!itotal*!}
\xdef\jdesign{*!jdesign*!}
\xdef\jdesignbis{*!jdesignbis*!}
\xdef\jqte{*!jqte*!}
\xdef\jpu{*!jpu*!}
\xdef\jtotal{*!jtotal*!}
\xdef\kdesign{*!kdesign*!}
\xdef\kdesignbis{*!kdesignbis*!}
\xdef\kqte{*!kqte*!}
\xdef\kpu{*!kpu*!}
\xdef\ktotal{*!ktotal*!}
\begin{document}
\include{template/facture_contenu}
\end{document}
    """

    for cle, valeur in data.items():
        recherche = '*!' + cle + '*!'
        template = template.replace(recherche, valeur)

    return(template)


# ecriture du fichier tex
def ecriture_fichier_tex(fichier_tex, contenu_tex):
    with open(fichier_tex, 'w') as fp:
        fp.write(contenu_tex)

# conversion latex en PDF
def convert_pdf(fichier_tex):
    commande = f"pdflatex -interaction=nonstopmode -halt-on-error -output-directory {batch_dir} {fichier_tex} > /dev/null"
    os.system(commande)

# programme principal

while True:
    # Recupération des fichiers JSON
    json_fichiers = glob.glob(input_dir + '*.json')
    for json_fichier in json_fichiers:
        fichier_base, extension = os.path.splitext( os.path.basename(json_fichier) )
        # print(json_fichier, fichier_base, extension)

        data = lecture_json(json_fichier)

        # creer contenu de la facture
        contenu_tex = creer_facture_tex( data )

        # ecriture fichier latex
        fichier_tex = batch_dir + '/' + fichier_base + '.tex'
        ecriture_fichier_tex(fichier_tex, contenu_tex)

        # conversion en PDF
        convert_pdf(fichier_tex)

        with tarfile.open(
            f"{archive_dir}{fichier_base}.tgz", 
            "w:gz", 
            compresslevel = 9
            ) as tf:
            move_to_tar(f"{input_dir}{fichier_base}.json", tf)
            move_to_tar(f"{batch_dir}/{fichier_base}.log", tf)
            move_to_tar(f"{batch_dir}/{fichier_base}.tex", tf)
            os.remove(f"{batch_dir}/{fichier_base}.out")
            os.remove(f"{batch_dir}/{fichier_base}.aux")

            # deplacer le fichier PDF
            shutil.move(f"{batch_dir}/{fichier_base}.pdf", f"{doc_dir}/{fichier_base}.pdf")

        print(f"Conversion terminée {fichier_base}")

    # Attendre x secondes avant de reprendre la boucle
    time.sleep(20)

