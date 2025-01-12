from core import Solver, algorithms
import shutil
if __name__ == "__main__":
    # Nombre de tentatives
    num_attempts = 10
    best_score = 310000


    # Réinitialiser le solver
    solver = Solver("./challenges/d_final.in", './sortie.txt', False, [], 'EBMIPS')


    for attempt in range(num_attempts):
        print('--------------------------------------------------------')
        print(f"\nTentative {attempt + 1}/{num_attempts}")
        
        solver.trajectories = []
        solver._history_score = []
        solver.algorithm = algorithms.Algorithm.factory('EBMIPS', solver.datamodel )
        print(solver.trajectories)

        # Exécuter les calculs
        solver.run()
        solver.post_process()
        
        # Récupérer le score actuel
        current_score = solver.get_totalscore()  # Assurez-vous que cette méthode existe dans Solver
        print(f"Score obtenu : {current_score}")
        
        if current_score > best_score:
            #best_score = current_score
            best_file = f"output_{current_score}.txt"

            # Sauvegarder le fichier sous le nom correspondant au score
            # Faire une copie du fichier
            copy_file = f"{best_file}"
            shutil.copy('./sortie.txt', copy_file)

            print(f"\033[42Nouveau meilleur score !\033[0 Fichier enregistré sous : {best_file}")
        else:
            print("Pas de nouveau meilleur score.")
        print('--------------------------------------------------------')

    print(f"\nMeilleur score final : {best_score}. Fichier associé : {best_file}")