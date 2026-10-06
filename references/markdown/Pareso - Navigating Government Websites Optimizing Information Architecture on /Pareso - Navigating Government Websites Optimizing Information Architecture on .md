# Pareso - Navigating Government Websites Optimizing Information Architecture on 


<!-- Page 1 -->

Navigating Government Websites: Optimizing
Information Architecture on the US Department
of Labor Site
Fiorella Falconi(B) , Arturo Moquillaza , Adrian Lecaros , Joel Aguirre ,
Carlos Ramos , and Freddy Paz
Pontiﬁcia Universidad Católica del Perú, Av. Universitaria 1801, San Miguel, Lima 32, Lima,
Perú
{ffalconit,adrian.lecaros,aguirre.joel,
carlos.ramosp}@pucp.edu.pe, {amoquillaza,fpaz}@pucp.pe
Abstract. Government websites serve as sources of information and services
related to public affairs, playing an essential role in connecting citizens with gov-
ernment institutions. The responsibility of government websites extends beyond
just providing information; they must ensure that the information is easily acces-
sible and understandable. This paper analyzes and redesigns the United States
Department of Labor’s website. The research began by examining user-generated
content on social media and online forums, shedding light on user grievances and
challenges. The analysis revealed a signiﬁcant issue with the website’s information
architecture, causing users to need help ﬁnding the information they needed. A
heuristic evaluation was conducted, and issues related to problems with usability
heuristics, including “Help and documentation,” “Visibility of system status,” and
“Aesthetic and minimalist design,” were also identiﬁed. To initiate the redesign, a
virtual card sorting activity engaged potential users to reorganize content and cat-
egories. User interface (UI) components were developed, presenting a fresh color
palette aligned with the Department of Labor’s branding. Remote Usability Testing
(RUT) with seven diverse users, leading to further reﬁnements for responsiveness
and consistency. Usability tests on the prototypes demonstrated the value of a
user-centric approach. If implemented on the United States government website,
this redesign could alleviate user pain points, particularly information accessi-
bility. In conclusion, optimizing government website information architecture is
vital for improving user experience. This research and redesign process serves as
a valuable case study for enhancing the usability of government online platforms,
ultimately beneﬁting citizens and their interactions with government services.
Keywords: E-Government · User-centered design · Architecture information ·
Prototyping · Human-Computer Interaction · User Experience
© The Author(s), under exclusive license to Springer Nature Switzerland AG 2024
A. Marcus et al. (Eds.): HCII 2024, LNCS 14712, pp. 38–52, 2024.
https://doi.org/10.1007/978-3-031-61351-7_3

<!-- Page 2 -->

Navigating Government Websites 39
1 Introduction
Government websites play a pivotal role in providing information related to public
affairs in countries. Users seeking information or some procedure on these websites
often have limited alternatives, as governmental institutions are the primary sources of
such information and services [ 24, 25].
Government websites are often the only source of information, procedures, or ser-
vices on a wide range of topics, from taxation and employment to healthcare and social
services.
Users of these websites bring diverse needs and expectations, ranging from infor-
mation acquisition to seeking assistance and access to essential services. In the digital
age, where users have unrestricted access to global information, citizens are aware of
the disparities in government-provided services [ 1].
Consequently, it is imperative that government websites are meticulously designed
with a focus on usability, credibility, and accessibility. These factors are signiﬁcant as
they impact how citizens utilize and embrace e-government services and shape their
daily interactions with e-government websites.
Historically, the origins of government websites can be traced back to the pioneering
efforts of internet entrepreneur Eric Brewer, who set the stage for the inception of the
ﬁrst government website known as Firstgov.gov in 1999 [ 2]. Over time, these initial
portals have evolved from rudimentary search engine counterparts into sophisticated
platforms, bolstering their capabilities with advanced search functionalities, enriched
content offerings, and enhanced user control [ 3].
Due to particular dynamics that emerged after the pandemic in the workplace that
showed a tight and competitive labor market with rates of vacant positions and res-
ignations [ 26], the importance of verifying the usability that users had to deal with
when navigating the United States Department of Labor’s website. The Department
of Labor’s website, as it exists today, emerged in 2009, stemming from the efforts of
the Wirtz Labor Library, which began collecting and providing access to select agency
websites associated with the department [ 4]. Presently, this portal assumes a pivotal
role as a comprehensive resource for information and services pertinent to employment,
labor laws, and workforce development. The department’s overarching mission revolves
around “fostering, promoting, and developing the welfare of wage earners, job seek-
ers, and retirees in the United States.” It is dedicated to improving working conditions,
advancing employment opportunities, and ensuring work-related beneﬁts and rights [ 5].
To accomplish this formidable mission, it is indispensable that the website’s design and
functionality align with the diverse needs of its user groups. This paper is structured
as follows: An introduction and the theoretical framework to understand the essential
concepts of this paper; the third chapter starts to explain the process and the user research
executed to understand the website’s pain points. This research includes Heuristic eval-
uation, card sorting, and usability testing. The fourth chapter explains the prototyping
process performed for mobile and desktop versions. The ﬁfth chapter explains how the
test of the interactive prototype was designed and the tasks the seven users had to execute.
In the last two chapters, we explain the test made on the ﬁnal prototypes and the results.
Also, we explain the importance of the user-centered design on government websites.

<!-- Page 3 -->

40 F. Falconi et al.
2 Theoretical Framework
This chapter delves into the theoretical framework and concisely explores foundational
elements, offering insights into the key theoretical dimensions that shape modern digital
governance experiences.
2.1 User-Centered Design
User-centered design process (UCD) is also known as a human-centered design process
[6], where development proceeds with the user as the center of focus [ 7]. The central
goal of this framework is to develop an optimal product that aligns with user needs,
steering away from imposing a product’s features on users and tailoring the design to
enhance user satisfaction and functionality [ 8].
2.2 E-government
E-Government is the reference for electronic government because governments at the
local, regional, and national levels worldwide are responsible for harnessing this capa-
bility to establish an electronic presence [ 9]. E-government entails leveraging informa-
tion and communication technologies, especially web-based applications, to facilitate
quicker, simpler, and more efﬁcient access to and delivery of information and services
to the public [ 10].
Given the importance of e-government, the United Nations published an E-
Government Survey, the sole worldwide report evaluating the e-government progress
of the 193 UN Member States. Its purpose is to function as a resource for countries to
exchange insights, recognize strengths and challenges in e-government, and inﬂuence
their policies and strategies [ 11].
2.3 Information Architecture
The usability.gov website explains Information Architecture (IA) as focusing on organiz-
ing, structuring, and labeling content effectively and sustainably [12]. The key objective
in constructing a website’s IA is establishing a coherent and user-friendly knowledge
system, ensuring that content is easily locatable and accessible for users [13]). To achieve
this objective, there are some speciﬁc tools related to IA: Content inventory, Taxonomy
development, card sorting, tree testing, and usability testing, among others.
The author L. Rosenfeld, mentions the difﬁculty of mapping the boundaries of the
IA and speciﬁes that we can’t confuse Information architecture with Graphic design,
software development, or usability engineering [ 14].
2.4 Heuristic Evaluation
The heuristic evaluation is an evaluation that helps us to identify problems in how a
system’s interface works. We can do this by following clear guidelines. The main goal
of the evaluators is based on the use of rules called heuristics, which look at the design

<!-- Page 4 -->

Navigating Government Websites 41
to spot these problems [ 15]. The author Lecaros explains, based on Nilsen, that for the
execution, it’s best to have 3 to 5 evaluators for the most value. Each person checks
independently, and when they’re done, they compare results to get an overall view of
usability [16].
2.5 Card-Sorting
Card sorting is a tool to help understand the users for whom we are designing something
[17]. The proper deﬁnition is that this tool is a UX research technique where participants
group labels written on notecards based on criteria that make sense to them. Figure 1
shows the basic steps to perform card sorting. This method reveals how the target audi-
ence organizes their knowledge and helps create an information architecture aligned
with users’ expectations [18].
Fig. 1. Card-sorting process (extract from [ 17])
2.6 Responsive Design
The growing population of internet users and the prevalence of mobile devices, such as
smartphones and tablets, have generated a necessity to customize the content presented
on each device. Responsive design is identiﬁed by its ability to dynamically adjust content
to ﬁt the screen size, ensuring a favorable viewing experience on any web access device
[19]. To achieve maximum usability and impact, a website’s content should intelligently
re-shaped itself [ 20].
3 Process and User Research
Göransson et al. (2003) presented a detailed usability design process encompassing three
phases. However, for this redesign, only the ﬁrst two signiﬁcant phases were taken into
account, as the development aspect of the redesign was beyond the scope. Figure 2
illustrates the adapted process implemented in this redesign effort.
To commence the user-centered design process, the information gathering and
research phase was initiated to identify pain points and improvement opportunities on
the DOL’s website. As a ﬁrst step, a review of the current website was conducted to
understand the number of pages and the material covered. The examined website is
hosted at https://www.dol.gov/ [21].
Given the extensive user base of this website, input was gathered from forums and
social media, where users shared real difﬁculties encountered while interacting with the

<!-- Page 5 -->

42 F. Falconi et al.
Fig. 2. Process redesign for the DOL website
website in search of speciﬁc information. Since this information is public and freely
accessible, an analysis of these comments was performed, helped by word cloud gener-
ators and search engines associated with the web, revealing a common theme of users
searching for information on the web, not ﬁnding it, and subsequently attempting to
contact other points of contact within the Department of Labor. Additionally, the topics
most frequently referenced by social media users in their searches were identiﬁed. The
results indicated that users recurrently sought information on pages such as the Contact
DOL page, Unemployment Insurance, Continuation of Health Coverage, and Frequently
Asked Questions.
Based on these results, two evaluations were conducted: a remote usability test with
potential users and a heuristic evaluation. The usability test, conducted with 7 participants
using the Useberry tool, revealed that only 4 participants could complete all assigned
tasks, and the average time to complete the tasks was 5 min. Figure 3 displays the results
obtained in the Useberry tool format.
Furthermore, pain points identiﬁed from the usability test included the following:
 The website information is hard to recognize and understand for ﬁrst-time users.
 The navigation menu and labels are not descriptive enough to quickly ﬁnd what users
are searching for.
 Too many links listed make it overwhelming to use the website.
 Users are uncomfortable using the website due to the technical language.
Table1 presents the issues identiﬁed in the pages analyzed in the heuristic evaluation.
With these research ﬁndings, a clearer panorama emerged regarding why users face
difﬁculties and the speciﬁc usability issues that need resolution.

<!-- Page 6 -->

Navigating Government Websites 43
Fig. 3. Usability test results
The research ﬁndings revealed the need for a signiﬁcant overhaul of the website’s
information architecture, navigation, and language. Key improvements included are the
following:
 Streamlined Information Architecture: Reorganizing website content into a clear and
intuitive hierarchy, making it easier for users to locate the information they need.
 Enhanced Navigation: Redesigning the navigation menu with descriptive labels and
drop-down menus to facilitate quick and efﬁcient access to speciﬁc sections.
 Simpliﬁed Language: Replacing complex jargon with plain language to improve
comprehension and accessibility for all users.
A remote card-sorting session was conducted using the FigJam tool to reorganize
the website’s information architecture. Participants were tasked with grouping content

<!-- Page 7 -->

44 F. Falconi et al.
Table 1. Heuristic problems on the DOL website
ID Heuristic Problem Description
P01 Help and documentation The search option doesn’t show suggestions
while typing
P02 User control and freedom The main navigation bar doesn’t remain on the
page’s top while scrolling
P03 Help and documentation Navigation menu labels are not very clear,
especially to ﬁrst-time users
P04 Help and documentation Labels are not clear in every instance.
Sometimes, they overwhelm and create confusion
P05 Visibility of system status Webpages redirect users to a different platform
with different navigation and system status
P06 Error prevention There is no clear way to go back or return to the
homepage
P07 Aesthetic and minimalist design It is challenging to scan through the content.
There is no clear section breakdown
P08 User control and freedom Labels take the user in an unknown direction
they believed should remain in the same category and assigning an appropriate name to
each category. The results can be seen in Fig. 4.
Fig. 4. Remote card sorting

<!-- Page 8 -->

Navigating Government Websites 45
4 Prototyping
Prototypes are widely recognized as a foundational method for exploring and expressing
designs for interactive computer artifacts [ 22]. They serve as a visual tool to illustrate
the evolution of a design and experiment with different concepts.
Using the Figma tool, we developed prototypes for this redesign ranging from low
to high ﬁdelity. This choice was informed by the team’s pre-existing knowledge and
the ease of creating interactive prototypes for future usability testing. Key highlights
implemented in the medium-ﬁdelity prototypes included:
 Utilizing the hero space to showcase important news with brief descriptions, aiming
to provide users with quick and easy access to the latest information.
 Introducing new categories in headers and labels.
 Designing drop-down menus to display options within each category, enhancing
navigation and information retrieval.
 Standardize the internal pages’ design with the homepage and incorporate bread-
crumbs to aid navigation.
A glimpse of some design proposals is depicted in Figs. 5 and 6.
Fig. 5. Mid-ﬁdelity Main Page
Medium-ﬁdelity prototypes were also created for the mobile version. To ensure a
responsive design, we implemented the following changes:

<!-- Page 9 -->

46 F. Falconi et al.
Fig. 6. Mid-ﬁdelity Internal Page
 We prioritized displaying the main categories using a layout more suitable for a
mobile screen. We retained the desktop version’s dropdowns and utilized typography
to highlight internal options.
 The search component was repositioned after the menu, allowing users to search if
the desired information is not found manually.
 The footer was redesigned to incorporate social media links and language assistance.
Table 2 presents the proposed design decisions to solve the pain points founded on
the research.
To validate the user comprehension of the content within the redesigned pages and
the ease of identifying new components, a 5-s test was conducted. This method, based
on Gronier’s protocol [23], involves the following:
1. Introducing the context of the page that users will assess.
2. Informing users that they will see a page for 5 s and should try to remember everything
in that short time.
3. Displaying the page for precisely 5 s.
4. Prompting users to share everything they recall and explaining how they could
accomplish a speciﬁc task.
The feedback obtained from this test guided improvements to be implemented in the
high-ﬁdelity interactive prototype, as shown in Fig. 7. Some established enhancements
include:

<!-- Page 10 -->

Navigating Government Websites 47
Table 2. Design decisions related to pain points.
Problem Description Design Proposal
Information is hard to recognize and difﬁcult to
navigate menú
Architecture information restructuration
There are too many links listed Links are grouped by categories and with
the help of images
Difﬁculty in language translation Highlight the bilingual options by placing
them at the beginning
Redirection to different pages with different
navigation
Use the same layout of components and
breadcrumbs for all pages
There is no clear way to go back to the homepage The home option is always available
The search option doesn’t show suggestions
while typing
Help display content while writing
The main navigation bar disappears with
scrolling
Stick the bar always to have the options
available
 Dividing the hero image into three sections to display more news simultaneously;
hovering over the image reveals additional information.
 Placing language assistance within the header facilitates access for those seeking the
Spanish version.
 Adjusting font sizes for better visualization.
 Add a blog section, Twitter, Contact Us, and federal government websites to the
homepage.
5 User Testing
After the high-ﬁdelity prototypes are prepared and interactive, the next step involves
planning the usability test and deﬁning the tasks that users will perform during the test.
For this usability test, three tasks were formulated based on information gathered
from forums and social media, where the most sought-after information by real users
was analyzed. The deﬁned tasks were as follows:
 Find the phone number to call for information.
 Locate information about the Continuation of Health Coverage (COBRA) on the
website.
 Review the main page and identify the different sections.
 The test was strategically planned to be conducted remotely to engage a larger pool
of participants. In total, the test was administered to 7 users.
6 Results and Findings
After we ﬁnished the seven tests, the data was processed, and the insights were clustered.
The outcomes were as follows:

<!-- Page 11 -->

48 F. Falconi et al.
Fig. 7. Hi-ﬁdelity Main DoL page

<!-- Page 12 -->

Navigating Government Websites 49
 All seven users successfully located information in the dropdown menus, ﬁnding the
experience intuitive.
 All seven users noted consistency across the two website versions.
 Four users faced challenges in reading certain texts.
 Two users expected to ﬁnd the site map under the “About Us” category.
Fig. 8. Hi-ﬁdelity iterations
Responding to these ﬁndings, a subsequent iteration was deemed necessary to address
the identiﬁed pain points from the usability test. The following improvements were
implemented:
 We increased the font size for menu options to 18px.
 We altered the position and layout of trending topics.
 We included the site map option within the “About Us” category without removing
it from the footer.

<!-- Page 13 -->

50 F. Falconi et al.
 We incorporated the language assistance option in the header of the mobile version.
The ﬁnal prototype, showcasing these four modiﬁcations post-usability test, is
illustrated in Fig. 8.
7 Conclusions and Future Works
In conclusion, optimizing the information architecture of government websites is cru-
cial to ensure users can access the information and services they need. This research
and redesign process on the US Department of Labor’s website serves as a valuable case
study for improving the usability of governmental online platforms, ultimately beneﬁt-
ing citizens and enhancing their interactions with government services. The user-centric
approach, encompassing analyses of user-generated content, heuristic evaluations, and
usability testing, unveils a strategic roadmap for addressing challenges in government
website design. By prioritizing usability, this research contributes to the broader under-
standing of the evolving signiﬁcance of government websites and underscores their
pivotal role in fostering effective citizen-government interactions.
Government websites are indispensable hubs for citizens seeking information and
services related to public affairs, and their design signiﬁcantly inﬂuences user experi-
ences. In acknowledging the limitations of current government websites, this research
advocates for a proactive and user-centered redesign approach. The Department of
Labor’s website, a critical resource, becomes a testing ground for implementing vital
improvements. The iterative analysis, redesign, and usability testing process offers valu-
able insights into the multifaceted nature of user interactions with government platforms.
This case study is relevant to the Department of Labor and provides a broader framework
for enhancing the usability of government websites, aligning them more closely with
citizens’ evolving expectations.
In future works, the insights gleaned from this research and redesign process open
avenues for future exploration in enhancing various government websites. Analyzing
and improving the usability of governmental online platforms is an ongoing endeavor,
and the success of the Department of Labor’s website redesign provides a blueprint for
similar initiatives.
Acknowledgments. The authors thank all the participants involved in this experience, which has
allowed the development of the present work. This study is highly supported by the HCI, Design,
User Experience, Accessibility & Innovation Technologies Research Group (HCI-DUXAIT).
HCI-DUXAIT is a research group of the Pontiﬁcia Universidad Católica del Perú (PUCP).
References
1. Prins, J.E.J.: Electronic government. variations on a concept. In: Prins, J.E.J. (ed.) Designing
E-Government: On the Crossroads of Technological Innovation and Institutional Change 1–5.
Kluwer Law International (2001). ISBN 978–9041116215
2. Department of Labor. USAGov’s mission and History. Department of Labor (2023). https://
www.usa.gov/mission-history

<!-- Page 14 -->

Navigating Government Websites 51
3. Gant, J., Gant, D.B.: Web portal functionality and state government e-service. In: Proceedings
of the 35th Hawaii International Conference on System Sciences (2003). https://doi.org/10.
1109/hicss.2002.994073
4. Department of Labor. Website archive. DOL (2023). https://www.dol.gov/general/aboutdol/
history/digital-archive
5. Department of Labor. About us. DOL (2023). https://www.dol.gov/general/aboutdol
6. Shawn Lawton Henry and Justin Thorp. Notes on User-Centered Design Process (UCD).
W3.org (2004). https://www.w3.org/W AI/redesign/ucd
7. Rubin, J.: Handbook of Usability Testing: How to Plan, Design, and Conduct Effective Tests.
John Wiley and Sons, Inc (2008)
8. Argumanis, D., Moquillaza, A., Paz, F.: Challenges in integrating SCRUM and the user-
centered design framework: a systematic review. En Commun. Comput. Inf. Sci. 6(6), 52–62
(2020) https://doi.org/10.1007/978-3-030-66919-5_6
9. Huang, Z.H., Benyoucef, M.: Usability and credibility of e-government websites. Gov. Inf.
Q. 31(4), 584–595 (2014). https://doi.org/10.1016/j.giq.2014.07.002
10. Lee, J.: 10year retrospect on stage models of e-Government: a qualitative meta-synthesis.
Gov. Inf. Q. 27(3), 220–230 (2010). https://doi.org/10.1016/j.giq.2009.12.009
11. United Nations. New global survey shows e-government emerging as a powerful tool
(2023). https://www.un.org/en/desa/new-global-survey-shows-e-government-emerging-pow
erful-tool
12. Department of Health and Human Services. Information Architecture Basics (2023). https://
www.usability.gov/what-and-why/information-architecture.html
13. Tankala, S.: Information architecture vs. sitemaps: What’s the difference? Nielsen Norman
Group (2023). https://www.nngroup.com/articles/information-architecture-sitemaps/
14. Rosenfeld, L., Morville, P .: Information Architecture for the World Wide Web. Inc, O’Reilly
Media (2002)
15. Nielsen, J.: Usability Engineering. Morgan Kaufmann Publishers Inc., San Francisco (1993)
16. Lecaros, A., Paz, F., Moquillaza, A.: Challenges and Opportunities on the Application of
Heuristic Evaluations: A Systematic Literature review. In: Soares, M.M., Rosenzweig, E.,
Marcus, A. (eds.) HCII 2021. LNCS, vol. 12779, pp. 242–261. Springer, Cham (2021).https://
doi.org/10.1007/978-3-030-78221-4_17
17. Spencer, D., Garrett, J.J.: Card sorting: Designing Usable Categories. Rosenfeld Media (2009).
ISBN 978–1933820026
18. Sherwin, K.: Card Sorting: Uncover users’ mental models for better information architecture.
Nielsen Norman Group (2018). https://www.nngroup.com/articles/card-sorting-definition/
19. Almeida, F., Monteiro, J.: The role of responsive design in web development. Webology
14(2), 157 (2017). http://www.webology.org/2017/v14n2/a157.pdf
20. Subic, N., Krunic, T., Gemovic, B.: Responsive web design – Are we ready for the new age?.
Online J. Appl. Knowl. Manag. 2(1), 93–103 (2014). https://www.iiakm.org/ojakm/articles/
2014/volume2_1/OJAKM_V olume2_1pp93-103.pdf
21. Department of Labor. DOL (2023). https://www.dol.gov/
22. Houde, S., Hill, C.: What Do Prototypes Prototype? In: Handbook of Human-Computer
Interaction (2nd Ed.), Helander, M., Landauer, T., Prabhu, P . (eds.): Elsevier Science (1997).
https://doi.org/10.1016/B978-044481862-1.50082-0
23. Gronier, G.: Measuring the ﬁrst impression: testing the validity of the 5 second test. J. Usability
Stud. 12, 8–25 (2016). https://doi.org/10.5555/3040226.3040228
24. Cabinakova, J., Kroenung, J., Eckhardt, A., Bernius, S.: The Importance of Culture, Trust,
And Habitual Patterns - Determinants of Cross-Cultural Egovernment Adoption (2013). ECIS
2013 Completed Research. 182. http://aisel.aisnet.org/ecis2013_cr/182

<!-- Page 15 -->

52 F. Falconi et al.
25. The World Bank. Digital Government for Development. The World Bank. IBRD. IDA.https://
www.worldbank.org/en/topic/digitaldevelopment/brief/digital-government-for-development
26. Domash, A., Summers, L.H.: How Tight are U.S. Labor Markets? (2022). https://doi.org/10.
3386/w29739