
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="logo.png" alt="Logo" width="80" height="80">
  <h1 align="center">CRUSTACEA</h1>
  <p align="center">
    A ten fingers typing training TUI-App in python based on TEXTUAL!
    <br />
    <a href="https://github.com/ManuelSchenk/crispy-crustacea/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/ManuelSchenk/crispy-crustacea/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>
<br />

<!-- ABOUT THE PROJECT -->
## About The Project

This Application is for people who wants to learn or improve there ten fingers typing skills.
You can use your own texts or scripts in your favorite programming language with common syntax highlighting to get faster and more efficient in your everyday working.

<div align="center">
    <img src="crustacea.png" alt="Logo" width="924" height="751">
</div>

#### It provides the following features:
* an terminal based editor 
* uses the color theme of "vscode_dark"
* syntax highlighting for the most programming languages with tree-sitter
* provides live statistics about your typing performance
* multiple options are provided like "auto tabbing" and "force a backslash after a typing failure"
* you can enable cursor navigation to jump to the part of your file you want to train with 

#### Example TUI visualisation:
<div align="center">
    <img src="example.png" alt="Logo" width="915" height="634">
</div>
 
Of course, the app do not provide all features i have planed (see [[roadmap]]) or you are looking for now since your needs may be different. 
So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. 

<br />

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

* Install Python 3.13
* Install Poetry

### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/ManuelSchenk/crispy-crustacea.git
   ```
2. Change into the project directory
   ```sh
   cd crispy-crustacea
   ```
3. install environment with poetry
   ```js
   poetry install
   ```
4. run CRUSTACEA with python
   ```sh
   poetry run python ./crustacea/main.py
   ```



<!-- USAGE EXAMPLES -->
## Usage

To run CRUSTASEA with your own script use the following command:  (TODO)
   ```sh
   poetry run python ./crustacea/main.py <path to your script>
   ```

In the Footer you see all the options which can be toggled in and out with keyboard shortcuts:
* `ctrl+s` - **Pause Timer, if you want to make a break while training on a text**
* `ctrl+b` - **Disable the default behavior: if your make a typing fault you have to correct it with Backspace**
* `ctrl+t` - **If your press Enter at the end of a line you jump to the next not empty line. If want to type the TABS manually you can use this**
* `ctrl+n` - **Enables the Cursor Navigation, so you can jump to the next part of your text you want to train your skills on**


<!-- ROADMAP -->
## Roadmap

- [ ] enable arguments with **typer** to choose the file you want to train with
- [ ] store the results/scores in a sqlite and visualize the history of your last results 
- [ ] provide beginners lections with reduced key set (create the example text with chatGPT)

See the [open issues](https://github.com/ManuelSchenk/crispy-crustacea/issues) for a full list of proposed features (and known issues).




<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- CONTACT -->
## Contact

Manuel Schenk - [linkedin-url](linkedin-url)

Project Link: [https://github.com/ManuelSchenk/crispy-crustacea](https://github.com/ManuelSchenk/crispy-crustacea)



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This app is built on [Textual](https://textual.textualize.io/), an innovative framework from **Will McGugan** that empowers developers to create modern, interactive, and highly customizable terminal user interfaces. Leveraging Python’s asynchronous capabilities and the advanced rendering features of the Rich library, Textual streamlines the development of dynamic, responsive, and visually engaging TUI applications.

For more information and resources, please refer to the following documentation:
- [Textual Documentation](https://textual.textualize.io/)
- [Textual GitHub Repository](https://github.com/Textualize/textual)
- [Textual Tutorials](https://textual.textualize.io/tutorials/)

---


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-url]: https://github.com/ManuelSchenk/crispy-crustacea/issues
[linkedin-url]: https://www.linkedin.com/in/manuel-schenk-48246117a/
[product-screenshot]: crustasea.png



