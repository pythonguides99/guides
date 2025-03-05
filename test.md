# Creating-A-Project-Planning-And-You
---------------------------------------------------------------------------------------
Planning A New Project:
When creating a project plan, add a cover page, use headers and bullet points and add a contents page / table to aid readbility
Be consistent with headers
Watch your SPAG
Make it all relevent to the project you are designing
---------------------------------------------------------------------------------------
Part A - Project Proposal:
---------------------------------------------------------------------------------------
both parts in 20 hours, 10 -10 split at worst but try for closer to 7-13 cause the design takes longer
Business Context:
SWOT analysis of project
Naming + explanation of stakeholders in project
---------------------------------------------------------------------------------------
Requirements:
list of requirement name, brief description, essential or desirable
Functional requirements (what program needs to do)
Non-functional requirements (not features but things it needs, e.g security & speed)
decomposition of requirements (in depth explanation of how they work / how they will be implemented)
----------------------------------------------------------------------------------------
Key Performance Indicators And Use Cases:
KPIs (list KPIs and give a small explanation, KPIs = things you can use to judge performance e.g number of bug reports or time spent on a screen)
User acceptance criteria (list and give a small explanation, user acceptance = what the user expects to be able to do with the program e.g log into an account)
Use cases (short examples of a task and the steps that a user would take to do it)
----------------------------------------------------------------------------------------
Description Of Proposed Solution:
A short paragraph giving an explanation of the project and what it aims to achieve
----------------------------------------------------------------------------------------
Risks And Risk Mitigation:
Give risks relevant to the specfic project as well as general ones
Risks - give examples and explanations of risks to the developement / success of the project
Risk mitigation - give examples and explanations of how these specific risks will be mitigated
-----------------------------------------------------------------------------------------
Regulations, Legal And Ethics:
Laws & Legislations:
give exampels of diferent laws and legislations and how they are relevant to the project
give general digital ones like GDPR but also ones specific to the project like health laws for a health app
Ethical Considerations:
give different ethical considerations around the project (e.g ethics of giving out health advice) as well as ideas on how to deal with them
-----------------------------------------------------------------------------------------
Appendix:
add the appendix of research done (not sure on this still)
-----------------------------------------------------------------------------------------
Other Stuff:
Discuss how the planned project will meet industry standards and the use of emerging technologies
----------------------------------------------------------------------------------------
Part B - The Design:
----------------------------------------------------------------------------------------
Visual / Interface Design:
wireframes of each of the main pages of the solution 
can use figma, conva or other similar tools
use comments and labels to help better explain
make design good
use whitespace
use visual hierarchy?
-----------------------------------------------------------------------------------------
Algorithms:
Use both flowcharts and pseudocode to create some of the main systems from the program
do a good few
include error handling and stuff
dont make it too technical (dont use a load of technical terms or make it like code or anything)
----------------------------------------------------------------------------------------
Data Requirements:
Entity Relationship Diagram - diagram that does the database design
Data flow diagram - diagram of how the data flows between different parts and processes of the program (level 0/1)
Use case diagram - diagram with different users of the system and what they can do (add an explanation bit underneath)
Data dictionary - table outlining the variables used in the ERD, what they are for, their data type, length, error handling etc
-----------------------------------------------------------------------------------------
Test Strategy/Plan:
List all the components of the progam to be tested
list the prerequesites and dependencies needed to test each part
list the different types of testing that will be done (e.g security, funcitonality, integrating testing)
give brief description of the tests done for each test type (e.g functionality testing is check input validation, check error handling, etc)
-------------------------------------------------------------------------------------------

Part B - Creating The Prototype:

-------------------------------------------------------------------------------------------
general stuff: 
coding the program
need to follow the plan but do need to strictly stick to it
2 languages (c# & SQL)
interface good
include good  comments
use lots of error handling
use input / data validation
keep namimg conventions simple, short and relevant
use functions and classes where possible
------------------------------------------------------------------------------------------
programming notes:
-----------------------------------------------------------------------------------------
SQL:
sql connection string:
string connectionString = "Data Source = (LocalDB)\\MSSQLLocalDB; AttachDbFilename = file path ; Integrated Security = True; Connect Timeout = 30"; 
SqlConnection sqlConnection = new SqlConnection(connectionString);
sql command:
SqlCommand command = new SqlCommand("command name", sqlConnection); 
command.CommandType = CommandType.StoredProcedure; 
passing paramters to sql command:
command.Parameters.AddWithValue("@parameter", variable);
using insert, update, delete commads:
sqlConnection.Open(); 
command.ExecuteNonQuery(); 
sqlConnection.Close(); 
using select command (putting it into datatable):
SqlDataAdapter sd = new SqlDataAdapter(cmd);
sqlConnection.Open(); 
sd.Fill(datatable name); 
sqlConnection.Close(); 
stored procedures:
Create procedure [dbo].[procedure name] 
( 
@param1 type, 
@param2 type 
) 
as 
begin 
sql command
End 
insert:
insert into table name values @param1, @param2 
select:
select * from table name (where____ if neccessary)
delete:
Delete from table name (where___ if neccessary) 
update:
Update table name 
set column=@param1, 
column=@param2 
(where___ if neccessary)
--------------------------------------------------------------------------------------------
APIs:
private const string API_KEY = " API KEY HERE";
string Url = "http://api.openweathermap.org/data/2.5/forecast?" (<--- replace with API site url) + "q=" + city (<-- parameters) + "&mode=xml&units=metric&APPID=" + API_KEY;
getting data from API:
            // Get the response string from the URL. 
             (function-->)GetForecast(**client.DownloadString(ForecastUrl)** (<-- important bit)); 
        } 
        
        // Display the forecast. 
        private void GetForecast(string xml) 
        { 
            // Load the response into an XML document. 
            XmlDocument xmlDoc = new XmlDocument(); 
            xmlDoc.LoadXml(xml);  (<--- putting data from API into xml document)

              foreach (XmlNode timeNode in xmlDoc.SelectNodes("//time (API header thing)")) 
            { 
                // Get the time in UTC. 
                DateTime time = DateTime.Parse(timeNode.Attributes["from"].Value); 
                // Get the temperature. 
                XmlNode tempNode = timeNode.SelectSingleNode("temperature (subsection of each data entry)");
                string temp = tempNode.Attributes["value"].Value; (<--- specific bit of data from subsection)
                // Get the temperature. 
                XmlNode windSpeedNode = timeNode.SelectSingleNode("windSpeed"); 
                string windSpeed = windSpeedNode.Attributes["mps"].Value; 
                
![image](https://github.com/user-attachments/assets/bd4f5caa-f3a9-49b4-9dc7-202ca9996181)

                ^what the API data page thing looks like, useful for figuring out what to put when getting data from the xml
---------------------------------------------------------------------------------------------
general:
empty text box:
txtPeople.Text = string.Empty; 
conditionals:
if ((username==checkUser) && (password==checkPass)) <-- condition 1 AND condition 2
! <- not condition
^ <- XOR
|| <- OR
getting rows from datatable:
foreach (DataRow dr in datatablename.Rows) 
datatype variablename = (cast data type)(dr["column name"]); - regular get from datatable
string variable = dr["column"] != DBNull.Value ? (string)(dr["column"]) : "N/A"; - conditional get from datatable (gets data, if column for that row is blank, sets it as "N/A")
make sure to do anything with the data in the foreach loop
radio buttons:
private void chkTempFilter_CheckedChanged(object sender, EventArgs e) <--- event for when a radiobutton is checked / unchecked
            var TempRadioButtons = gbxTempFilters.Controls.OfType<RadioButton>();  <---- put at the top of the program, where the initialize is, gets all radiotbuttons in specified group box and stores them together
            foreach (RadioButton item in TempRadioButtons) 
            { 
                item.CheckedChanged += TempFilters_CheckedChanged; 
            } 
            
            string checkedName = ((RadioButton)sender).Name;  <-- use these in the checked change event to detect which ones are checked or not and do stuff baesd on that
            if (checkedName == "rbtnSpeedGreater") 

             if (rbtnGreaterTemp.Checked) <-- conditional based on if radiobutton is checked, works for check boxes as well

add visual basic to project:
![image](https://github.com/user-attachments/assets/0394bcbe-2493-4c7b-b7ee-cd097f5942e8)
right click on the project name, go to add, go to references, search for microsoft visual basic
string input = Interaction.InputBox("Prompt", "Title", "Default"); <-- code for input box
error handling:
try - catch - finally
try {} <- block of code
catch (exception e) {} <- block of code to do on exception catch, can specify what exception to catch and can have multiple catches for different exceptions
finally {} <- executes block after try - catch regardless of outcome
----------------------------------------------------------------------------------------------------
Multiple forms:
make second or third or fourth, etc, etc form
give it a name
CreateAccountForm create = new CreateAccountForm(); <--- put this at the top of the program to create the new forms (replace names with your own)
do this for every form you need
 private void btnLogIn_Click(object sender, EventArgs e) <- button click
 {
     if (logIn.ShowDialog() <- opens the form with the dialogue option == DialogResult.OK <- if the result on page close is OK) <- conditional using the result from the form
     {
         MessageBox.Show("Successful Log In");
         this.Hide(); <- makes the form invisible but does not close it entirely (closing the initial form1 just shuts the entire program down)
         if (main.ShowDialog() == DialogResult.OK)
         {
             this.Close(); <- fully closes the relevant form
         }
     }
 }

if (check) <- put this stuff at the end of the new form(s) code
both options close the current form down 
dont need both can just have ok or close
{ 
    this.DialogResult = DialogResult.OK; <- can be used for conditionals in the program that called the form to open
}
else
{
    this.DialogResult= DialogResult.Cancel;
}
use sql databases for transmitting data between forms (its just easier this way)
if you wanna put text in textboxes between forms use this:
public static TextBox test = new TextBox(); <- put this at the top of the code to create a textbox variable
        private void Form1_Load(object sender, EventArgs e)
        {
            test = txtTest; <- put this in the form load event and set the variable to the name of a textbox in the form
        }

        Form1.test.Text = "test"; <- put this in the other form (replacing names as neccessary) to put the text into the textbox
        same thing might work for other variables but its dubious
-----------------------------------------------------------------------------
documentation of process:
as going along and making the program, take screenshots of the code and the outputs and put them in a document, add comments to the document to help explain the code and whats happening a bit more
do it logically, in order
use it to show iterative developement of the program
---------------------------------------------------------------------------
testing:
follow the test plan and test the prototype, leave this till near the end but leave yourself some time to do the testing and make adjustments based on it
test the things you said in your test plan, doing a bunch of different tests
include whats being tested and the result of the test
include any notes such as things you realised or things your going to change based on the test
retest parts that have been changed
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

Task 3A - gathering feedback:

--------------------------------------------------------------------------------
