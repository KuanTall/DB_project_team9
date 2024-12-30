# DBMS final project

## About the Project
The mobile game Pokemon Go has gained massive popularity around the world, with over 80 million players still actively catching Pokemons every day 8 years after its launch. However, not every player is familiar with its battle mechanics. Therefore, for our project, we have decided to design an application to help players around the world to determine which Pokemons they should use in order to win faster and easier!

### Main Idea
When choosing the best Pokémon for a battle, several factors come into play, with type advantage and CP values being the most important ones. In this application, users will specify the Pokémon they are facing, and it will recommend Pokémons that have type advantages over the selected opponent.
Additionally, users can add their own Pokémon to the database and search through their personal Pokémon list for recommendations.

## Data
We utilized 3 data sets from Kaggle.
- the Pokemon list https://www.kaggle.com/datasets/shreyasur965/pokemon-go?resource=download
- the relationships between types https://www.kaggle.com/datasets/shreeyananda/pokemon-go-type-effectiveness
- skills and their type https://www.kaggle.com/datasets/thiagoamancio/full-pokemons-and-moves-datasets

We revised our plan regarding how to separate data into tables to better fit our sql designs. The data sets are now separated into 4 tables, with two additional tables storing user information and inputs. The following list highlights the changes we made:
- We decided to leave out “rarity” from the “pokemon” table when developing our project, but we kept the data in the table.
- We updated the “max_cp” values from the “pokemon” table since most of the values from the data set were incorrect. We also added “902” to “pokemon_id” since it was missing, and replaced the blank spaces in column “type2” with “None”.
- We rearranged the format of the “type” table to fit our sql, and we added type “None” to fit the changes to the “pokemon” table.
- We decided to drop the “acquire” table since it mostly contains information that would change with every event or season updates. It would be very hard to maintain this table, and we wouldn’t want to provide false/outdated information.
- We split the “skill” table into “skill” and “skilltype” since the contents of the original “skill” table come from different data sets.
- We added rows into the “skilltype” table to ensure every skill that appears in “skill” also appears in “skilltype”.

### Table Descriptions
- Pokemon: contains the id, name, max cp, and type of the Pokemons from the first data set.
- Type:  contains the relationships between different types from the second data set.
- Skill: contains the names of the skills that each Pokemon owns from the first data set.
- Skilltype: contains the names and types of skills.
- Account: stores the user account names and passwords.
- User: this table stores the user inputs, including the user id, the id and the cp values of the Pokemons they have.
### Features in Action
[Provide examples or screenshots of how to use key features.]

## Contributing
Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add YourFeatureName"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/YourFeatureName
   ```
5. Open a Pull Request.

## Acknowledgements
[List any resources, contributors, or tools that helped in the development of your project.]

## Contact
For any questions or suggestions, please reach out to:
- Name: [Your Name]
- Email: [Your Email]
- GitHub: [Your GitHub Profile]

