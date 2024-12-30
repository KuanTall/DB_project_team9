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

### Table Descriptions
- Pokemon: contains the id, name, max cp, and type of the Pokemons from the first data set.
- Type:  contains the relationships between different types from the second data set.
- Skill: contains the names of the skills that each Pokemon owns from the first data set.
- Skilltype: contains the names and types of skills.
- Account: stores the user account names and passwords.
- User: this table stores the user inputs, including the user id, the id and the cp values of the Pokemons they have.

## Installation
### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/BK5008/DB_project_team9.git
   ```
2. Navigate to the project directory:
   ```bash
   cd DB_project_team9
   ```
3. Install dependencies:
   ```bash
   pip install flask mysql-connector-python
   ```
4. Access MySQL:
  ```bash
   mysql -u [your_username] -p
   ```
5. Create the database:
   ```sql
   CREATE DATABASE pokemon;
   ```
6. Use the database:
   ```sql
   USE pokemon;
   ```
7. Execute the `create_table.sql` script to set up the database tables:
   ```sql
   SOURCE create_table.sql;
   ```

## Usage
### Running the Application
1. Start the application:
   ```bash
   python3 main.py
   ```
2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
## Application features
### Searching
When selecting the Pokemon they want to search for, users can either choose from the drop-down list or manually enter its ID. If the check button is selected, the query will only include Pokémon from the 'user' table that match the corresponding user ID. Otherwise, the query will include all Pokemons in the “pokemon” table.

### My Pokemon
Users can manage their own Pokémon and search for those available for use.

## Contribution
- 郭紘宇: data preprocess, query design, interface design.
- 曾冠羲: backend design, interface design.

## Links
- Discussion: https://g0v.hackmd.io/@BK5008/H143lzHgJe
- Repository: https://github.com/BK5008/DB_project_team9.git
- Video:
