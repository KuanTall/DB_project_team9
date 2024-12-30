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
![tables](Image/1.png)
![table relation](Image/2.png)

## Database
We used MySQL as our database. We used the templates from HW3 to develop our webpages, and the webpage structure is designed as below, with “welcome.html” containing the application of searching, insertion, update and deletion. After the execution of the above functions, it will redirect back to the welcome page.

![database](Image/3.png)

We will explain the implementation of each part as follows.
- The login/signup mechanics are the same as in HW3.
- In the welcome page, we will first perform a query to show the user’s Pokemon list in the “My Pokemon” session.

![In the welcome page](Image/4.png)

- The drop-down lists are handled by the get_options function. It will perform a query to access Pokemon IDs and names, fetch them, and then load them into the drop-down list.

![The drop-down lists](Image/5.png)

- The option chosen by the user from the drop-down list will be stored in variable “selected_option”, while the values the user entered in the text field will be stored in variable “search_input”. These two variables, along with a boolean variable “owned” indicating if the check button is selected, will be sent into the “search_result” function.
- In “search_result”, if “owned” is true, the My Pokemon version of the query will be performed. Otherwise, the global search version will be performed. If the user chooses one option from the list but enters another ID in the text field, the input from the drop-down list will take priority.
- When pressing “add” button, similar to searching, the backend takes the username, the option(ID) user selected from the drop-down list and the new cp value from the text field, incorporates them into the insertion query, sends them to the database, and then redirects back to the page.
- When pressing “update” button, the backend takes the username, the ID value from the same row as the update button and the new cp from the text field, incorporates them into the update query, sends them to the database, and then redirects back to the page.
- When pressing “delete” button, the backend takes the username, the ID value from the same row as the delete button, incorporates them into the update query, sends them to the database, and then redirects back to the page.
- The queries are included and explained in the following parts.
- Since all the user inputs are either from the drop-down list or from entering numbers in the text field, there is not a lot of room for exceptions. We still perform a type conversion into integers to ensure the inputs are numbers.

## Application features
### Searching
Users must sign up and log in before using our application. The design of the signup and login pages follows the templates provided in HW3.
The main application page is divided into two sections. The upper half includes the following components:
- A “welcome” title and a brief description of our application.
- Log out and search buttons.
- The flash message block.
- A drop-down list allowing users to select the Pokemon they want to search for, and a text field where users can manually enter the ID of the Pokemon.
- A check button that allows users to choose whether to search globally or limit the search to their own Pokemon list.
- A display area for the search results.

![Searching](Image/6.png)

When selecting the Pokemon they want to search for, users can either choose from the drop-down list or manually enter its ID. If the check button is selected, the query will only include Pokémon from the 'user' table that match the corresponding user ID. Otherwise, the query will include all Pokemons in the “pokemon” table.

![Searching query](Image/7.png)

The query design for global search is as above. We first retrieve the skills and their corresponding types for each Pokemon by joining the “skill” and “skilltype” tables. We then join the outcome with the “pokemon” table.

In the “WHERE” clause, we first filter out the Pokemons who have type disadvantages toward the target Pokemon to prevent the Pokemons we recommend from getting easily defeated in battles. We then make sure the Pokemons left have at least one type that is effective against the target Pokemon. Finally, we verify the skills presented are of the same type as the recommended Pokemons. All “%s” would be replaced by the target Pokemon’s ID.

We use the “GROUP BY” clause to limit the outcome and make sure the recommended Pokemon only appears once. Since the “GROUP BY” clause only allows aggregate functions to be selected, we chose MAX(skillname) for the skill name column. The result includes 10 recommended pokemons and is ranked by their max cp.

![Searching result](Image/8.png)

When the check button is selected, we perform a different query to search from the user’s Pokemon list.

![Searching my pokemon](Image/9.png)

This query searches from the user’s Pokemon list by joining the “user” table and “pokemon” table, and outputs the cp of the user’s Pokemon instead of max cp. The rest of the query follows the same structure as the one for global search.

### My Pokemon
The bottom half of the application page includes the following components:
- A “manage my pokemon” title.
- A drop-down list and a text field where the user can specify the ID and cp of the Pokemon they want to add.
- A display of the user’s Pokemon list ranked by cp. Each row includes an update button, a delete button, and a text field for the user to enter the updated cp value.

![manage my pokemon](Image/10.png)

![crud](Image/11.png)

The queries for insertion, update and deletion all follow the basic structure. Since the user inputs should be numbers only(ID or cp), we implemented a type conversion to make sure the inputs are numbers. If not, we will output a warning in the flash message block.

![command](Image/12.png)

## Schdule
![schdule](Image/13.png)

Since some of the data sets contained incorrect information or had formats that didn’t fit well into query designs, we spent extra time on correcting the data and rearranging the format of the tables.

## Contribution
- 郭紘宇: data preprocess, query design, interface design.
- 曾冠羲: backend design, interface design.

## Links
- Discussion: https://g0v.hackmd.io/@BK5008/H143lzHgJe
- Repository: https://github.com/BK5008/DB_project_team9.git
- Video:
