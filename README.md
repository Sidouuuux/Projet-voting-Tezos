# Projet-voting-Tezos
Le smart contract de vote qui permet à plusieurs utilisateur de voter:

        •	2 vote  possible ("yes"  or "no" )

        •	Tous les utilisateurs ont le droit de voter

        •	Un utilisateur doit pouvoir ne voter qu'une seule fois

        •	Le contrat doit avoir un super utilisateur (admin) et son addresse est initialisé au déploiement du contrat

        •	L'administrateur n'a pas le droit de voter

        •	Le smart contrat doit être mis en pause si 10 personnes ont voté.

        •	Quand le smart contract est mis en pause , le resultat du vote doit être calculé et stocké dans le storage.

        •	L'administrateur doit pouvoir remettre à zéro le contrat (effacer les votes) + enlever la pause

Installation nécessaire :

        • Ligo tools : https://ligolang.org/docs/intro/installation/
        • Tezos : https://tezos.gitlab.io/introduction/howtoget.html#build-from-sources

Compilation du contrat :

        • ligo compile-contract voting_contract.ligo main > voting_contract.tz

Simuler le contrat :

        • ligo dry-run --sender=tz1VPFYwwtWZ5ytH5ZcMYyvqi9AmiR3d8sJT voting_contract.ligo main 'SetAdmin(("tz1VPFYwwtWZ5ytH5ZcMYyvqi9AmiR3d8sJT":address))' 'record balanceofvotes=map("tz1VPFYwwtWZ5ytH5ZcMYyvqi9AmiR3d8sJT":address) -> True;end; owner=("tz1VPFYwwtWZ5ytH5ZcMYyvqi9AmiR3d8sJT":address); contractPause=False;yesVotes=0;noVotes=0;end'

Tester le contrat :

        • pyetest testcontract.py
