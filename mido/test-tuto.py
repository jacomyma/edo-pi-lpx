import mido;

print("1. == SCAN Ports MIDI-IN/OUT accessibles à MIDO/RTMIDI sur le PC ==")
print("Scan Ports Midi-OUT des équipements accessibles à RtMidi-IN...")
print(mido.get_input_names(),"\n")
print("Scan Ports Midi-IN des Équipements accessibles à RtMidi-OUT...")
print(mido.get_output_names(),"\n")

# ***** ACQUISITION MIDI-IN / MIDO-RTMIDI *****
# Test de réception de messages MIDI envoyés par Roland PC-200 à M-Audio Uno MIDI/USB
#   puis de RtMidi-In (Thru) vers RtMidi-Out qui les renvoie vers Qsynth/FluidSynth
print("2. == Boucle Acquisition + Affichage Messages envoyés par Clavier physique ==")
outport = mido.open_output('RK005:RK005 MIDI 1 28:0') # connexion RtMidi-Out à Synth-In
with mido.open_input('Launchpad X:Launchpad X MIDI 2 24:1') as inport: # connexion RtMidi-In à M-Audio-Out
    for msg in inport: # passe contenu 'inport' à 'msg'
        if msg.bytes() != [144, 36, 0]: # teste touche Do2 ON/OFF pour sortir boucle acquisition
            outport.send(msg) # envoie contenu 'msg' à RtMidi-Out vers Synth-In
            print("Humain: ", msg) # affiche contenu 'msg' Humain à l'écran
            print("  Bytes décimal:", msg.bytes()) # affiche contenu 'msg' Bytes à l'écran
            print("  Bytes hexadéc:", msg.hex()) # affiche contenu 'msg' Bytes à l'écran
            # ATTENTION: chaque "print" introduit du retard dans le jeu temps réel
            #   des notes jouées. Il faut structurer le script en conséquence.
        else:
            outport.reset() # envoie "All notes off" + "Reset all controllers" sur chaque canal
            # outport.panic() # stoppe toutes notes qui sonnent mais sans RàZ des contrôleurs
            outport.close() # ferme le port RtMidi-Out proprement
            if outport.closed: # test si port bien fermé
                print("\nLe port RtMidi a bien été fermé !")
            print("\nTouche DO 2 appuyée puis relachée = EXIT !", msg.bytes())
            print("ACQUISITION MIDI-IN TERMINÉE...")
            # Le port RtMidi-IN a été fermé automatiquement à la fin de la procédure with...as 
            exit() # arrête le script avec demande confirmation (fonction IDE utilisé)
