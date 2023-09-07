# VRBZO HUP Generator

This package provides a solution for generating a new HUP (Handhaving Uitvoerings Programma) for the VRBZO (Veiligheidsregio Brabant-Zuidoost) project exectued by me under the name of ClickLogic.

## Note
This repository is a cleaned-up version of the original repository used during development. In the spirit of opensource development compromising or proprietary information has been removed to allow public publishing. Please contact me if you need access to the original repo. 

## Branches

- **main branch**: Contains all files necessary for local development, including context information about the project.
- **production branch**: Intended for deployment and distribution purposes. Made obsolete by Releases.

## How it Works

The VRBZO HUP Generator follows a specific workflow for generating and distributing the HUP. Here are the steps involved:

1. **Development**: Start with the `main` branch for development. This branch contains all the required files and context information related to the project. Perform local development and testing using this branch.

2. **Generate Executable**: When ready to compile the project, generate a new executable using the development environment. This executable is named "main" and is the result of compiling the project.

3. **Production Branch**: Switch to the `production` branch. This branch serves as the production-ready branch and is meant for distribution and use.

4. **Copy Executable**: Copy the compiled executable file (named "main") from the development environment and place it in the `production` branch. This ensures that the latest version of the executable is available for distribution.

5. **Distribution**: Distribute the `production` branch to the intended users. No need to have python installed, just share the folder. Make sure that it is a main folder with two sub folder namely data and HUP. The new HUP will be output in the HUP folder. Source data should be placed in the data folder with names like this: "KRO-aanzien-R22.csv" & "KRO-gebruik-R22_zonder-contact.csv". This can be changed in the original Python file main.py. 

By following this workflow, you can easily manage the development and deployment of the VRBZO HUP Generator.

## Usage

To use the VRBZO HUP Generator, follow these steps:

1. Clone or download the `production` branch to your local environment. Or more easily, get the executable from Releases!

2. Run the executable file named "HUP_Generator" to generate the new HUP. See the required file structure in point 5 in the "How it Works" section above.

3. Distribute the generated HUP file to the appropriate stakeholders as per your project requirements.



## License

This project is licensed under the MIT License.

Feel free to explore the provided branches and use the VRBZO HUP Generator for your specific needs.

If you encounter any issues or have questions, please don't hesitate to reach out.

Happy generating!
