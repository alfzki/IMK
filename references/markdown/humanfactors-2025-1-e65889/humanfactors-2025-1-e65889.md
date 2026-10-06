# humanfactors-2025-1-e65889


<!-- Page 1 -->

Original Paper
Co-Designing a Web-Based and Tablet App to Evaluate Clinical
Outcomes of Early Psychosis Service Users in a Learning Health
Care Network: User-Centered Design Workshop and Pilot Study
Kathleen E Burch1, BA; Valerie L Tryon1, PhD; Katherine M Pierce1, PhD; Laura M Tully1, PhD; Sabrina Ereshefsky1,
PhD; Mark Savill1,2, PhD; Leigh Smith3, PhD; Adam B Wilcox4, PhD; Christopher Komei Hakusui1, BA; Viviana E
Padilla1, BA; Amanda P McNamara5, MPH; Merissa Kado-Walton5, MPH; Andrew J Padovani6, PhD; Chelyah
Miller1, BA; Madison J Miles1, BA; Nitasha Sharma1, BA; Khanh Linh H Nguyen1, MS; Yi Zhang6, PhD; Tara A
Niendam1, PhD
1Department of Psychiatry & Behavioral Sciences, University of California-Davis, Sacramento, CA, United States
2Department of Psychiatry and Behavioral Sciences, Weill Institute for Neuroscience, University of California-San Francisco, San Francisco, CA,
United States
3Department of Psychology, University of California-Davis, Davis, CA, United States
4Institute for Informatics, Washington University in St. Louis, St. Louis, MO, United States
5Herbert Wertheim School of Public Health and Human Longevity Science, University of California San Diego, San Diego, CA, United States
6Center for Healthcare Policy and Research, University of California-Davis, Sacramento, CA, United States
Corresponding Author:
Kathleen E Burch, BA
Department of Psychiatry & Behavioral Sciences
University of California-Davis
4701 X St
Sacramento, CA, 95817
United States
Phone: 1 916 699 5193
Email: knye@ucdavis.edu
Abstract
Background: The Early Psychosis Intervention Network of California project, a learning health care network of California
early psychosis intervention (EPI) programs, prioritized incorporation of community partner feedback while designing its eHealth
app, Beehive. Though eHealth apps can support learning health care network data collection aims, low user acceptance or adoption
can pose barriers to successful implementation. Adopting user-centered design (UCD) approaches, such as incorporation of user
feedback, prototyping, iterative design, and continuous evaluation, can mitigate these potential barriers.
Objective: We aimed to use UCD during development of a data collection and data visualization web-based and tablet app,
Beehive, to promote engagement with Beehive as part of standard EPI care across a diverse user-base.
Methods: Our UCD approach included incorporation of user feedback, prototyping, iterative design, and continuous evaluation.
This started with user journey mapping to create storyboards, which were then presented in UCD workshops with service users,
their support persons, and EPI providers. We incorporated feedback from these workshops into the alpha version of Beehive,
which was also presented in a UCD workshop. Feedback was again incorporated into the beta version of Beehive. We provided
Beehive training to 4 EPI programs who then piloted Beehive’s beta version. During piloting, service users, their support persons,
and EPI program providers completed Beehive surveys at enrollment and every 6 months after treatment initiation. To examine
preliminary user acceptance and adoption during the piloting phase, we assessed rates of participant enrollment and survey
completion, with a particular focus on completion of a prioritized survey: the Modified Colorado Symptom Index.
Results: UCD workshop feedback resulted in the creation of new workflows and interface changes in Beehive to improve the
user experience. During piloting, 48 service users, 42 support persons, and 72 EPI program providers enrolled in Beehive. Data
were available for 88% (n=42) of service users, including self-reported data for 79% (n=38), collateral-reported data for 42%
(n=20), and clinician-entered data for 17% (n=8). The Modified Colorado Symptom Index was completed by 54% (n=26) of
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 1https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 2 -->

service users (total score: mean 24.16, SD 16.81). In addition, 35 service users had a support person who could complete the
Modified Colorado Symptom Index, and 56% (n=19) of support persons completed it (mean 26.71, SD 14.43).
Conclusions: Implementing UCD principles while developing the Beehive app resulted in early workflow changes and produced
an app that was acceptable and feasible for collection of self-reported clinical outcomes data from service users. Additional
support is needed to increase collateral-reported and clinician-entered data.
(JMIR Hum Factors 2025;12:e65889) doi: 10.2196/65889
KEYWORDS
eHealth; user-centered design; learning health system; psychosis; early psychosis; user-driven development; web-based; data
visualization; surveys and questionnaires; measurement-based care
Introduction
Background
Research estimates that the lifetime prevalence of psychotic
disorder diagnoses is approximately 1.5%, and the prevalence
of psychotic symptoms is between 4.2% and 17.5% [1].
California, the most populous and second most diverse state in
the United States [2], had a population of 39.11 million in 2023,
according to the California Census Bureau. This indicates that
586,650 to 6.8 million Californians may experience psychosis
symptoms in their lifetime. In response to this, many California
counties have developed specialty early psychosis intervention
(EPI) services, which vary widely in their implementation
approach [3]. The Early Psychosis Intervention Network of
California (EPI-CAL) [4] was developed to support the
provision of quality EPI services and to create an infrastructure
to conduct standardized measurement of the impact of early
psychosis care delivery. To support this goal, the EPI-CAL
team, in collaboration with several California counties,
developed a learning health care network (LHCN) consisting
of EPI programs across the state. The EPI-CAL LHCN later
joined the national Early Psychosis Intervention Network [5],
which allowed additional California EPI programs to participate.
Members of the LHCN agreed to gather standardized
information and outcomes from their clinics as part of
measurement-based care (MBC). Collecting this information
is critical to support quality early psychosis care provision within
clinical programs as well as enhance statewide learning and
development. For example, a narrative review of an MBC
approach in behavioral health clinics found such benefits as
significantly improving clinical outcomes, improving symptoms
more quickly, and decreasing treatment costs [6].
To this end, the EPI-CAL team chose to design and implement
a web-based and tablet app called Beehive. We chose the name
Beehive to reflect the envisioned purpose for the app: to help
LHCN programs learn and grow together for the betterment of
the collective, just as bees work together to build a hive for the
benefit of the colony. Beehive is a robust, stand-alone eHealth
app for use by service users, their support persons, and EPI
program providers. In this text, we use the term service user to
refer to the individual with a psychosis diagnosis who is
receiving mental health care from an early psychosis program.
We use the term support person to refer to any person that the
service user has chosen to involve in their care. This is typically
the individual’s parent but might be another family member, a
friend, a partner, or some other close relative. Beehive’s purpose
is to promote MBC in EPI programs by standardizing data
collection across a network of programs focusing on community
partner priorities; supporting key components of care such as
assessment, safety monitoring, and ongoing care delivery;
supporting program-level management of care; and aggregating
data across a large network to support evaluation and research
at state and even national levels [4].
We chose an eHealth approach to implementing MBC due to
its appropriateness for the EPI setting and its potential benefits.
Despite the perceived challenges related to experiences of
suspicion or paranoia, individuals experiencing mental health
difficulties, such as schizophrenia and bipolar disorder, have
widely found use of eHealth both feasible and acceptable [7-10].
Furthermore, the use of eHealth can support the advancement
of MBC. For example, eHealth apps have been previously
demonstrated to promote symptom and outcomes monitoring
in both early psychosis care [11,12] and LHCNs [13].
Conducting MBC with eHealth enhances its benefits as it allows
for data collection to be standardized across programs and
instantly available. For example, MBC may promote
collaboration across a care team [14-16], which is relevant for
EPI programs for which the evidence-based treatment,
coordinated specialty care, is inherently team based [17]. Use
of eHealth to collect data in this setting allows data collected
by one team member or entered by a service user to be instantly
available for all team members. eHealth also enhances the
benefits of MBC through data aggregation, which enables
evaluation of program performance [16,18,19] or promotion of
evidence-based treatments [16,20].
Though there are many potential benefits, there are also
numerous barriers to implementation of both new eHealth
technology and MBC. According to a systematic literature
analysis, the top factors posing a barrier to eHealth app
implementation include lack of digital health literacy, lack of
devices, financing issues, service-user cognition, and security
[21]. These barriers contribute to low adoption and user
acceptance, which limit the success of implementation [22,23].
Barriers to implementation of MBC include training burden,
concern that negative feedback causes harm to service users,
and the time required for survey completion [24-26].
To pursue the benefits of using eHealth to implement MBC and
mitigate the potential barriers, we developed Beehive with
user-centered design (UCD) principles. UCD prioritizes the
needs and expectations of the end user [27,28]. UCD approaches
include dedicated design activities, active involvement of users
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 2https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 3 -->

in the design process, incorporation of their feedback,
prototyping, and continuous evaluation [29], which can address
low user acceptance and low adoption [30]. Beehive’s iterative
development began with a collaborative process with service
users, support persons, and EPI program providers to identify
and prioritize which outcome measures should be collected in
the app [31]. We also explored how service users, support
persons, and EPI program providers wanted to be informed
about data-sharing options in Beehive and built Beehive’s end
user license agreement (EULA) workflow to incorporate user
perspectives [32]. With the survey content and EULA workflow
finalized, we moved onto the development of the user-facing
parts of Beehive.
Objectives
In this study, we aimed to (1) use UCD principles to create a
co-designed web-based and tablet app, called Beehive, to
support MBC in EPI programs, and (2) assess Beehive’s initial
feasibility in clinical settings by piloting it in 4 EPI programs.
Methods
Design
To promote Beehive engagement across multiple types of users
and across multiple domains of engagement, we integrated UCD
principles of incorporation of user feedback, prototyping,
iterative design, and continuous evaluation. Service users,
support persons, and EPI program providers had multiple
opportunities to provide feedback, which was incorporated
throughout Beehive development. Figure 1 shows the study
design from conceptualization through data collection.
Figure 1. Study design for Beehive development.
The development process began with conceptualization of user
journeys. User journey mapping envisions how specific types
of users, such as a service user or a service provider, will interact
with an app from access point through all required activities
[33]. User journey mapping allowed us to identify which
storyboards we should develop to present in UCD workshops
and which user-types we needed to recruit for those workshops.
Storyboards are a tool to visualize app workflows and the user
interface [34]. We developed storyboards to present as
prototypes in UCD workshops so that feedback could modify
the app design before time was invested in coding the alpha
version of the app. The alpha version of the app included core
workflows and was both evaluated internally and presented in
another UCD workshop to gather more feedback before coding
the beta version of the app. The beta version of the app
incorporated remaining feedback from storyboard workshops,
new feedback from the alpha stage, and added the remaining
core functionality that was not in-scope for the alpha version
(eg, reports). The beta version of Beehive was piloted by 3 EPI
programs over 6 months to further refine the app before
launching it across all EPI-CAL programs. We used pilot data
to assess initial use and uptake of Beehive’s beta version.
This UCD approach allowed the EPI-CAL team to receive and
incorporate feedback during conception, design, and testing
phases of eHealth app development, and include multiple
perspectives to facilitate user engagement in eHealth. Notably,
UCD has also been demonstrated to increase eHealth adoption
and user acceptance in research and clinical settings [30,35].
Participant Recruitment
UCD Workshops
For UCD workshops of the Beehive storyboard, we recruited
participants from the following three EPI community partner
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 3https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 4 -->

groups: (1) EPI service users, (2) their support persons, and (3)
EPI providers. Eligible participants were (1) actively or formerly
affiliated with an EPI-CAL EPI program, (2) English speaking,
and (3) able to provide written informed consent and assent
(minors or conserved adults). EPI program providers were
recruited through contact with the team lead of the 12 active
EPI-CAL EPI programs. Service users and support person
participants were invited either through EPI program provider
referral or by the research team directly contacting individuals
who had previously consented to be contacted for future research
opportunities.
One EPI-CAL clinic agreed to participate in a workshop for the
alpha version of the app to support the refinement of Beehive
before piloting.
Piloting
In total, 4 EPI-CAL clinics agreed to participate in 6 months of
Beehive beta testing before Beehive’s full launch across the
entire EPI-CAL LHCN. During this period, programs integrated
the Beehive app into standard clinical care. Pilot sites registered
service users who were active in their program at the time of
launching Beehive and new service users who started after the
launch. Each participating program has different acceptance
criteria for service users, and this has been described in a
separate protocol paper for the EPI-CAL study (NCT04007510)
[4]. Service users and support persons were excluded from
piloting if they did not speak English because Beehive beta
version was only available in English. At their first point of
contact with Beehive, service users and primary support persons
completed the Beehive EULA and were asked if they gave
permission for their clinical data collected in Beehive to be used
for research purposes [32]. We trained clinics to involve the
legal guardians of service users aged <18 during EULA
completion, and these service users were required to have a
primary support person registered in Beehive. Individuals could
update their data-sharing permissions at any time.
Methods
User Journey Mapping
The EPI-CAL research team worked collaboratively with the
contracted app developer in the user journey mapping and
storyboard design phases for the Beehive tablet and web apps.
Three primary user groups with distinct roles were identified:
(1) service users or support persons, (2) direct-service providers,
and (3) program administrators. Beehive user journeys were
developed for each group.
For all user groups, user journeys were designed to guide
individuals smoothly through Beehive onboarding and account
creation to the EULA explainer video detailing the types of
information Beehive collects, who can access their data, and
how to select their preferred permissions for who can view their
data [32]. Users then choose their data-sharing permissions.
Beehive then presents service users and support persons with
a series of one-time and longitudinal surveys to measure clinical
outcomes at 6-month intervals. Specific survey items associated
with risk, such as suicidal or homicidal ideation, send real-time
alerts to EPI program providers if they are endorsed by service
users. Beehive creates visualizations of this survey data. While
service users and support persons cannot independently access
survey visualizations, we considered this is as part of their user
journey because it should be shown to them by EPI program
staff as part of regular care.
EPI program provider user journeys were designed to facilitate
easy management of service user records and smooth navigation
to service user data. A dashboard presents the most important
information to users, such as outstanding survey alerts or other
action items. A client list presents all registered service user
records in list format with the most relevant information
displayed. EPI program provider users can click into service
user records to view survey results, survey visualizations, and
complete provider-entered surveys. Providers can display survey
results and survey visualizations as part of ongoing care with
service users and their support persons to facilitate
understanding and coordinate treatment priorities.
Administrator user journeys were designed to promote
clinic-level management tasks, such as Beehive implementation
and quality assurance. Administrator dashboards present
aggregate-level information of survey data and allow for the
ability to compare clinic averages to the average of the EPI-CAL
LHCN. Administrator dashboards also present summaries of
Beehive activity across the clinic. Administrator users can also
download reports, including survey data reports, to use their
clinic data for quality assurance or reporting requirements.
UCD Workshops
Next, the development team created dynamic storyboards of
the above user journeys. These storyboards were presented to
community partners from early psychosis clinics in 90-minute
UCD workshops. Figures 2 and 3 are images from the
storyboards presented to community partners.
In the storyboard workshops, we presented major features of
the app and asked for feedback on the app’s look and feel, as
well as functionality as it related to existing clinical workflow,
and ease of use and acceptability for service users, their support
persons, and EPI program providers. Because we determined 3
user-types during user journey mapping, we held 3 different
types of storyboard workshops tailored to the journeys of these
users: service users or support persons, direct-service providers,
and program administrators. If EPI providers had roles in both
direct-service provision and program administration, they could
attend both groups. UCD workshops were conducted through
videoconferencing to comply with the COVID-19 social
distancing restrictions. Each session was audio recorded and
included 2 facilitators (KEB, LMT, TAN, or SE) and a notetaker
(VLT). There were no other individuals present other than
researchers and participants. The notetaker took detailed notes,
as close to verbatim as possible. Audio recordings were used
as a reference to fix any portions of the notes which were not
clear.
After storyboard workshops, we integrated feedback to make
design changes to the alpha version of the app. During a
90-minute alpha testing workshop, we solicited feedback on
the alpha app, with a special emphasis on how compatible it
was with the existing clinical workflows. We created test
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 4https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 5 -->

accounts for each participant and had them complete various
core workflows in the app, such as registering a service user,
completing surveys, and reviewing data visualizations. This
workshop included one facilitator (KEB) and one notetaker
(LS). After the conclusion of all workshops, we continued to
integrate feedback to make design changes in the beta version
of the app.
Figure 2. Survey item in storyboard.
Figure 3. Clinical administrator dashboard in storyboard.
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 5https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 6 -->

Piloting
Finally, piloting of the beta version of Beehive was conducted
over a 6-month period with EPI-CAL LHCN programs that
were identified as pilot sites. We provided training to each pilot
site and assigned them a point person from our research team
to provide regular support, troubleshoot implementation
challenges, and escalate app bugs and implementation barriers.
We trained all program staff, regardless of clinical role. The
training series showed users how to complete key Beehive
workflows, introduced the EPI-CAL core assessment battery,
and included activities on how to interpret data visualizations.
We also met with key staff at each program to support them to
devise a plan to integrate Beehive into their existing clinical
workflows, such as how to integrate service user registration
during the clinical intake process. The full description of this
training and support is described in a separate paper [4]. During
this training and support process, we received informal feedback
from program staff about implementation successes and
challenges.
During piloting, programs integrated the Beehive app into
standard clinical care for all service users. Service users and
their support persons were registered in Beehive web app by
staff at their EPI program. Program staff entered the service
users’ treatment start date which was considered the start of the
service users’ baseline window in Beehive. At enrollment,
baseline, and every 6 months thereafter, surveys were assigned
to service users, their support person, and their provider.
One-time surveys assessing lifetime experiences were available
for all respondents at enrollment. Service users had 3 enrollment
surveys, support persons had 1, and clinicians had 1.
Longitudinal surveys were assessed at treatment baseline and
every 6 months thereafter. Service users had 17 longitudinal
surveys, support persons had 6 surveys, and clinicians had 9
surveys. The duration of baseline survey window was 60 days;
the duration of follow-up survey windows was 30 days (15 days
before and after the target completion date). Figure 4 shows a
Beehive training slide with a visualization of survey windows.
Figure 4. Beehive training slide showing survey windows during piloting.
Programs were instructed to enroll all service users, regardless
of how long they had been affiliated with the EPI program.
Therefore, some individuals may have been enrolled in Beehive
after their baseline window had closed, and their first time point
during piloting may have been a 6-month time point or a
12-month time point. Service users and support persons could
access and complete surveys in-person at the clinic on the tablet
app or they could complete them remotely via “web link.” The
“web link” was a unique link that was texted or emailed to them
weekly during survey windows if surveys were not fully
completed. Surveys accessed via web link could be completed
on any personal device that had access to the internet and a web
browser. Service providers completed surveys and could review
data on the web app. Baseline surveys were intended to support
the clinical intake process, including initial assessment and
collaborative treatment planning. Follow-up surveys were
intended to support ongoing assessment, adjustments to
treatment planning, and monitoring of treatment goals.
The EPI-CAL core assessment battery, including how it was
created and all included measures, is described in a separate
paper [4]. Briefly, Beehive survey content includes both the
Early Psychosis Intervention Network core assessment battery
[36] and additional measures based on EPI community partner
feedback determined in earlier qualitative work for the EPI-CAL
study [4,31]. A table of measures is included in the Multimedia
Appendix 1 [4]. One survey of particular interest is the Modified
Colorado Symptom Index (MCSI) [37], a measure central to
the aims of the broader EPI-CAL study and which we asked
sites to prioritize [4]. The MCSI is a 14-item, self-report scale
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 6https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 7 -->

which measures the frequency of psychiatric symptoms,
including symptoms of mood, psychosis, cognition,
forgetfulness, and risk to self and others. Respondents indicate
frequency of symptoms over the past 30 days on a 0 to 4 scale
of “not at all” to “at least every day.” Total scores range between
0 and 56, with higher scores indicating higher frequency and
number of psychiatric symptoms.
Data Analysis
In UCD workshops, we asked highly structured questions to
solicit feedback on the storyboard and alpha version of Beehive.
Subsequently, we organized our data categories relevant to the
workflows and features we were evaluating. We then organized
comments by whether they were supportive of the existing
features or critical and asked for change so that we could focus
on what features to move forward and what features to change
as we created the alpha and beta versions of Beehive.
To investigate the initial feasibility of Beehive in EPI-CAL
clinics, we reviewed descriptive statistics of pilot participants,
including registration, enrollment, participant characteristics,
and survey completion. Engagement with surveys and survey
completion were examined in three ways as follows: (1)
determine the proportion of service users for whom any data
were entered, regardless of respondent type, (2) determine the
rate of survey completion across all available surveys, and (3)
evaluate whether participants completed all, partial, or no
surveys across survey time points during piloting phase. Partial
survey completion indicates that the respondent completed at
least 1 survey, but did not complete all of their surveys in the
specified time point. We also evaluated completion of MCSI
because it is a measure that we asked programs to prioritize.
Ethical Considerations
The institutional review board of the University of California,
Davis, approved the study (1403828-21, California Collaborative
Network to Promote Data-Driven Care and Improve Outcomes
in Early Psychosis). In addition, several of the counties and
universities with a program participating in EPI-CAL required
a separate review and approval of the project by their
institutional review board. All study participants provided
written informed consent and assent (as appropriate).
Participants received US $30 compensation for each workshop
they participated in. Participants in the piloting phase were not
compensated because integration of Beehive was part of routine
care in the EPI program. Audio recordings UCD workshops
include voice print identifiers and are stored in compliance with
University of California, Davis HIPAA (Health Insurance
Portability and Accountability Act) policies and procedures.
Data collected during piloting for research includes limited
identifiers including zip code, dates of service, and month and
year of birth. Only trained research staff with a need-to-access
have access to identifiable data.
Results
UCD Workshops
We conducted 14 storyboard workshops with 77 total
participants between April 3, 2020, and August 28, 2020. In
total, 4 workshops were with service users (n=8, 10%) and their
support persons (n=9, 12%). In addition, 10 workshops were
with EPI program providers (n=60, 78%), including 6 for service
providers, 3 for administrators, and 1 for both service providers
and administrators. Demographics for workshop participants
are provided in Table 1.
We completed an interim analysis of storyboard workshop data
in May 2020. We completed the final analysis of workshop data
in August 2020, after all groups were completed. After each
analysis, we discussed and synthesized the feedback for the
developers to support app development. We attempted to balance
the needs of all types of participants. However, if there were
needs or feedback in direct contrast with one another, we
prioritized service-user feedback due to our value of centering
service-user feedback in this app. This feedback and the action
taken to address it are summarized in Table 2.
We conducted 1 alpha workshop in October 2020 with 4 EPI
program provider participants. Feedback from this workshop
was analyzed in October 2020. During this workshop,
participants identified a few bugs in the app, but their feedback
primarily focused on ideas for integrating Beehive into clinical
workflows. For example, they suggested that Beehive training
should include best practices for how providers can review the
data, engage with the data, and make the most out of Beehive.
They also shared concerns about using technology in telehealth
settings. For example, switching to telehealth in response to the
COVID-19 pandemic had been very difficult for some families,
and they predicted those same families would find using Beehive
challenging if the clinic could not meet with them in-person to
teach them how to use it. They were less concerned about
service users and support people using Beehive on a tablet in
the clinic where they could provide in-person support. Finally,
participants brought up the importance of shifting the culture
of clinics to view data collection as an important part of
treatment, not just an extra task where information is being
extracted from service users. For example, surveys should be
directly related to service-user recovery goals. Participants
discussed how visualizations could be used to demonstrate the
clinical utility of gathering these data. For example, 1 clinician
said they would want to use the graphs to point out the way a
service user is improving or doing better and that they would
want to highlight their strengths. Another participant cautioned
that some service users may not want to look at data
visualizations and that this should be an optional part of their
care. Figures 5 and 6 illustrate design changes present in the
beta version of app after the conclusion of all workshops.
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 7https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 8 -->

Table 1. Demographics of user-centered design workshopsa.
EPIb program providers (n=60)Support persons (n=9)Service users (n=8)
Clinic type, n (%)
30 (50)6 (67)7 (88)Medi-Cal
30 (50)<5 (<55)<5 (<63)Private insurance
36.25 (26-50)41.50 (14-60)22.50 (16-33)Age (y), mean (range)
Sex at birth, n (%)
43 (72)8 (89)<5 (<63)Female
17 (28)<5 (<55)6 (75)Male
Gender, n (%)
43 (72)8 (89)<5 (<63)Female
16 (27)<5 (<55)6 (75)Male
——c<5 (<63)Nonbinary
<5 (<8)——Missing
Race, n (%)
5 (8)—<5 (<63)African or African American or Black
6 (10)——Asian
33 (55)6 (67)<5 (<63)White or Caucasian
10 (17)<5 (<55)<5 (<63)Other
<5 (<8)<5 (<55)<5 (<63)More than one
<5 (<8)<5 (<55)—Missing
Ethnicity, n (%)
26 (43)5 (56)<5 (<63)Latinx
33 (55)<5 (<55)5 (63)Not Latinx
<5 (<8)——Missing
Sexual orientation, n (%)
5 (8)—<5 (<63)Bisexual or gay or lesbian
54 (90)9 (100)5 (63)Heterosexual
<5 (<8)—<5 (<63)Other
aCells with fewer than 5 individuals are masked to protect the identity of participants.
bEPI: early psychosis intervention.
cNot available.
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 8https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 9 -->

Table 2. Implementation of feedback from user-centered design workshops.
Solution implemented in alpha versionProblem or need identified in workshop
Brought in more color into the palette and added icons for visual informationThe color scheme and layout seemed “overly clinical”
Changed color and design to make it more prominentSome important aspects of the user-interface were too subtle, such as
the survey progress bar or the urgent clinical issues widget
Added this workflow to the web app so that EPI program providers may
complete it in advance of service users engaging with surveys
Service-user and support person registration were only available as
self-registration and could not be completed by EPI program providers
Added clinic-level visualizations for race, ethnicity, sex, gender identity, and
other demographic metrics
Clinic-level data for service-user demographics was not visualized
Added a toggle to individual-level visualizations so that users can turn on
the threshold information or comparative data if they want to see it, or turn
it off if they do not want to see it
Not all service users or support persons wanted to see score thresholds
or comparative data on clinical measures, but some did
Added feature that allows users to set which measure displays by default for
each service user
Service users might have differed on which individual-level survey
visualization they wanted to see by default on their data view page
Changed “homeless” to “without a permanent address” when assessing
housing status; changed “help” to “Ask for help” to make it clearer that se-
lecting button will alert the EPI program provider; changed “Diagnosis” to
“Primary diagnosis”
Some language used in the app needed to be clarified for users to un-
derstand what data was being collected or how certain features worked
Wherever possible, implemented dynamic text so the service user’s preferred
name shows throughout the app, rather than any specific word to denote
“service user”
Different programs used different words to refer to service users, and
individuals might have varied on their preference for what word to use
regardless of what their program tended to use
Added in visual indicator to show survey completion across multiple surveys
(not just while completing one individual survey)
Program staff wanted to see overall progress on completion of all sur-
veys at any given time point
Added in a visualization that shows individual items as well as the global
score
When visualizing a survey, they wanted to have more than just the
global score visualized. Also, they wanted a visualization that showed
responses to individual items
Added the ability to enter a display name for surveys (eg, “Family Impact”
instead of “Burden Assessment Scale”)
Service users and support persons might not have preferred the official
names for measures and might have preferred a more simplified title
Added a hover modal on survey titles to show the display name for the surveyEarly psychosis intervention program providers needed a way to see
both the official measure name as well as the display name
Design a web link solution which allows service users and support persons
to answer surveys remotely. A link to complete their surveys can be emailed
or texted to them
The provision of clinic services might have been fully remote for the
foreseeable future, and the current design of Beehive only allowed
service users and support persons to complete surveys on a tablet in-
person at the clinic
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 9https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 10 -->

Figure 5. Survey item in beta.
Figure 6. Clinical administrator dashboard in beta.
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 10https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 11 -->

Piloting
We conducted piloting of Beehive beta app between March
2021 and September 2021. Our training and ongoing support
of pilot sites allowed us to gather informal feedback about both
the training and the Beehive app. We used this feedback to make
adjustments in real time, when possible, or to plan for future
changes to Beehive.
We made real-time changes to the training approach in response
to program needs based on our observations and their feedback.
At the time of training pilot sites in early 2021, these EPI
programs were navigating constant uncertainty related to the
COVID-19 pandemic, including influx of service users,
uncertainty about work location, reduced workforce, etc. In
response to this environment, we found it necessary to ask sites
to focus on small implementation steps even though we trained
them on all available workflows. For example, we asked pilot
sites to initially focus on engaging service users and their
support persons to complete enrollment and complete surveys.
When that was mastered, we asked them to focus on engaging
new service users and support persons with Beehive during their
clinical intake process. Finally, toward the end of the piloting
period, we encouraged them to focus on entering EPI program
provider-entered data. Even if pilot sites registered existing
service users, they were asked to set the service user’s survey
baseline date to align with their start in the EPI program.
Therefore, some service users may have never been assigned
surveys during their baseline survey window.
During the piloting phase, 93 service users, 78 support persons,
and 86 service providers were registered across 4 clinics. Of
the 93 service users who were registered into Beehive by their
program, 59 (63%) completed the Beehive EULA during
piloting, including 48 (51%) individuals who gave permission
to use their data for research. Of the 78 support persons
registered to a service user in Beehive, 52 (66%) completed the
Beehive EULA, including 42 (54%) individuals who gave
permission to use their data for research. Of these 42 support
persons, 5 were excluded from analysis because the service user
they were registered with did not give permission to use data
in research, and we prioritize the data-sharing decision of the
service user regarding use of collateral data for research
purposes.
While most users entered at least one survey window during
the piloting phase, 3 were discharged from their program before
longitudinal surveys were available. Of the 86 service providers
registered, 78 (91%) completed the Beehive EULA, including
72 (84%) individuals who gave permission to use their data for
research. This information is presented in Figure 7.
Participant demographics and EPI program provider professional
background are provided for individuals who agreed to share
their data for research purposes in Tables 3 and 4. Of note, age
is missing for some EPI program providers and support persons.
This data was collected during registration, and this field was
not included in the first release of the beta version of the app.
Therefore, some users were not able to complete this field during
registration and did not return later to update it, yielding missing
data for 15 (36%) support persons and 37 (51%) EPI program
providers.
First, to examine engagement during piloting, we assessed the
number of service users that had entered any data that could be
used in care. During piloting, respondents entered survey data
for 85% (n=41) of service users. This includes self-reported
data for 75% (n=36), collateral-reported data for 42% (n=20),
and EPI program provider–entered data for 17% (n=8).
Second, we evaluated survey completion across the total amount
of available surveys. A total of 1517 surveys were assigned
across all respondent types during piloting and 35.4% (n=537)
of those surveys were completed across all time points. We also
evaluated survey completion by respondent type. Across all
time points, service users completed 396 (49.4%) of 802
assigned surveys. Support persons completed 113 (47.5%) of
238 assigned surveys. EPI program providers completed 28
(5.9%) of 477 assigned surveys.
Finally, we evaluated how many respondents completed all,
partial, or no surveys at each time point. Because participants
could be enrolled at any point in treatment, the first time point
for a service user may not have been their “baseline”
appointment. These data are presented in Table 5.
The MCSI was completed by 54% (26) of service users, and 7
were excluded for responses of “prefer not to say” (Total Score:
mean 19.58, SD 16.81). Additionally, 35 service users had a
support person who could complete the Modified Colorado
Symptom Index, and 56% (n=19) of support persons completed
it. From these 19, 5 were excluded for responses of “prefer not
to say” (mean 26.71, SD 14.43).
Through piloting, we also gathered informal feedback about
workflows that could be improved in Beehive and that we would
address with future change orders to the app after the testing of
the beta version of Beehive. For example, we received feedback
that the survey windows, initially chosen to mirror the data
collection windows of clinical trials, were far too narrow and
restrictive for data collection in community mental health
programs. Program staff users also indicated that they wanted
a better way of seeing a summary of what surveys service users
and support persons completed. Service user and support person
feedback was relayed to our team via program staff. For
example, service users and support persons wanted to customize
the day and time they received the web link via SMS text
messaging and email.
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 11https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 12 -->

Figure 7. Registration and enrollment during Beehive piloting.
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 12https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 13 -->

Table 3. Demographics of Beehive pilot participantsa.
EPIb program providers (n=72)Support persons (n=42)Service users (n=48)
33.89 (22-50)d44.11 (31-61)c18.88 (12-31)Age (y), mean (range)
Sex at birth, n (%)
30 (42)21 (70)24 (50)Female
5 (7)6 (20)24 (50)Male
—<5 (<12)—ePrefer not to say
37 (51)——Missing
Gender, n (%)
30 (42)21 (70)18 (38)Female
5 (7)6 (20)22 (46)Male
——<5 (<10)Nonbinary
——<5 (<10)Questioning or unsure of gender identity
37 (51)<5 (<12)<5 (<10)Prefer not to say
Race, n (%)
5 (7)7 (17)15 (31)African or African American or Black
——<5 (<10)American Indian or Alaskan native
8 (11)<5 (<12)<5 (<10)Asian
19 (26)<5 (<12)10 (21)Hispanic or Latinx only
33 (46)10 (24)10 (21)White or Caucasian
5 (7)<5 (<12)8 (17)More than one race
<5 (<7)——Other
—<5 (<12)<5 (<10)Prefer not to say
—<5 (<12)—Unsure
<5 (<7)12 (29)—Missing
Ethnicity, n (%)
41 (57)17 (40)27 (56)No—I do not identify as Hispanic or Latinx
28 (39)5 (12)14 (29)Yes—I identify as Hispanic or Latinx
—5 (12)5 (10)Unsure or do not know
<5 (<7)<5 (<12)<5 (<10)Prefer not to say
<5 (<7)12 (29)—Missing
Service user diagnosis, n (%)
———Clinical high risk
——6 (13)Attenuated psychosis symptoms
———First episode psychosis
——<5 (<10)Substance induced psychotic disorder with onset
during intoxication
——9 (19)Mood disorders with psychotic features
——10 (21)Schizoaffective disorder
(bipolar or depressive type combined)
——5 (10)Schizophrenia
——<5 (<10)Other specified schizophrenia spectrum disorder
——<5 (<10)Unspecified psychosis
——7 (15)Other first episode psychosis
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 13https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 14 -->

EPIb program providers (n=72)Support persons (n=42)Service users (n=48)
———Clinical high risk or first episode psychosis status
not confirmed
——<5 (<10)Anxiety disorders
Number of support persons registered in Beehive, n (%)
——14 (29)None
——29 (60)1
——5 (10)2
Relationship of support persons with service user, n (%)
—5 (12)—Parent (adoptive)
—34 (81)—Parent (biological)
—<5 (<12)—Stepparent
—<5 (<12)—Spouse or partner
—<5 (<12)—Sibling
aCells with less than 5 individuals are masked to protect the identity of participants.
bEPI: early psychosis intervention.
cData missing for 15 individuals.
dData missing for 37 individuals.
eNot available.
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 14https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 15 -->

Table 4. Professional background of early psychosis intervention program providers registered during Beehive pilot (N=72)a.
Values, n (%)Background
Education level
7 (10)HSb diploma or GEDc
<5 (<7)Associate’s degree
16 (22)BAd or BSe
18 (25)MAf or MSg
7 (10)MFTh
<5 (<7)MSWi
5 (7)PsyDj
6 (8)PhDk
9 (13)MDl
Professional role
<5 (<7)Administrative support staff
<5 (<7)Case manager or recovery coach
6 (8)Clinic coordinator
<5 (<7)Clinical supervisor or team lead
30 (42)Clinician or therapist
<5 (<7)Family advocate
<5 (<7)Peer support specialist
9 (13)Prescriber or psychiatrist or Other medical personnel
<5 (<7)Program director
<5 (<7)Research staff
<5 (<7)Supported education and employment specialist
7 (10)Other
Licensure status
49 (68)Unlicensed
23 (32)Licensed
Years licensed (n=23)
8 (38)≤1
7 (33)1 to 6
6 (29)≥7
Number of languages in which services are provided
47 (65)1
18 (25)2
7 (10)Missing
Languages for service provisionm
60 (92)English
18 (25)Spanish
<5 (<7)Arabic
<5 (<7)Hmong
<5 (<7)Tagalog
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 15https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 16 -->

Values, n (%)Background
<5 (<7)Other
aCells with less than 5 individuals are masked to protect identity of participants.
bHS: high school.
cGED: general educational development.
dBA: Bachelor of Arts.
eBS: Bachelor of Science.
fMA: Master of Arts.
gMS: Master of Science.
hMFT: Master of Marriage and Family Therapy.
iMSW: Master of Social Work.
jPsyD: Doctor of Psychology.
kPhD: Doctor of Philosophy.
lMD: Doctor of Medicine.
mRespondents could select more than one response, so percentages will be greater than 100%.
Table 5. Survey completion by respondent typea.
EPIb program providers, n (%)Support persons, n (%)Service users, n (%)
Survey completion at enrollmentc
10 (21)17 (50)30 (63)All
——d5 (10)Partial
38 (79)17 (50)13 (27)None
Survey completion at first time pointe
—17 (55)18 (40)All
4 (9)3 (10)8 (18)Partial
41 (91)13 (42)19 (42)None
Survey completion at second time pointf
——1 (33)All
———Partial
3 (100)2 (100)2 (67)None
aPartial survey completion indicates that respondents completed at least one survey, but did not complete all assigned surveys.
bEPI: early psychosis intervention.
cTotal respondents for service users, n=48; support persons, n=34; and service providers, n=48.
dNot available.
eTotal respondents for service users, n=45; support persons, n=31; and service providers, n=45.
fTotal respondents for service users, n=3; support persons, n=2; and service providers, n=3.
Discussion
Principal Findings
This study describes the EPI-CAL program’s design and
acceptability testing approach for a custom web-based and tablet
app, Beehive, to support systematic data collection, care
delivery, program evaluation, and research across a statewide
network of EPI programs. Our goal was to develop an app that
was clinically useful for, usable by, and acceptable to diverse
EPI programs across the state of California.
To ensure the app best matched the needs of the EPI participants,
we adopted a UCD approach to develop Beehive. Previous
research in the mental health digital space supports that active
involvement from the app’s intended users during the
development phase can improve the appropriateness of the end
product for the users of interest [38]. Initial feedback across the
3 development phases was primarily collected in workshops
(storyboard and alpha version) and during pilot implementation
(beta version). In storyboard and alpha workshops, we presented
prototypes to demonstrate major features of the app and asked
for feedback on the app’s “look and feel,” compatibility with
existing clinical workflow, and ease of use and acceptability
for service users, their support persons, and EPI program
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 16https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 17 -->

providers. Consistent with other studies who have included end
users during the design phase of their eHealth apps [38-41],
feedback from these workshops resulted in immediate changes
to the alpha and beta apps that would not have otherwise been
made.
During piloting, we continued to collect user feedback around
Beehive features, as well as assess acceptability of the app by
examining preliminary enrollment and survey completion. Our
enrollment and survey completion rates are consistent with the
acceptability of other mental health apps developed using a
UCD approach [42,43], although there is wide variability
depending on the implementation approach.
During the design and testing phase, we observed that different
types of community partners expressed different, and at times
conflicting, needs. For example, we asked participants about
their preferences for seeing score thresholds or comparative
data as part of the visualization for their clinical measures. Some
service users said that, in times of relapse or increasing intensity
of symptoms, additional information on the visualization would
be demoralizing. In contrast, many participants could imagine
scenarios where that information would be useful as a form of
psychoeducation to normalize service-user experiences or
understand the relative severity of symptoms. To address these
diverse needs and promote engagement with Beehive we added
a toggle to individual-level visualizations so that users can turn
the threshold information or comparative data on or off. A
flexible design approach that is tailored to an individual’s needs
has been shown to be more efficacious in a mobile health app
setting [43,44]. Therefore, design changes incorporated
flexibility where possible to enable our team to meet the various
needs of individuals while maintaining consistent
implementation to meet evaluation and research goals.
Similarly, user feedback informed our training approach. For
example, some EPI program provider users expressed that they
would use the graphs in the app in clinical care with service
users to highlight strengths and progress. In contrast, another
EPI program provider participant cautioned that some service
users may not want to look at data visualizations and that this
should be an optional part of their care. Thus, our training
approach highlights how visualizations may be used in direct
care but are not prescriptive. Feedback from workshop
participants also highlighted the importance of shifting clinic
culture to view data collection as a key part of care provision.
Our team considers EPI program providers to be integral in
promoting engagement for service users and their support
persons as it is the EPI program providers who communicate
why Beehive is being used in care. To begin addressing potential
barriers of buy-in and engagement for all users, we designed
our trainings to include the context of why Beehive and MBC
were being implemented in their programs, including a
presentation on the potential value of Beehive (designed and
delivered by author LS) [45].
During piloting, we observed barriers to integration. For
example, despite our designing the first training such that the
programs could start registering service users immediately
afterward, the programs failed to do so. When asked, programs
informed us that they were nervous to receive questions about
Beehive that they did not know how to answer. This resulted
in our team creating materials to provide more structure for
programs as they introduced Beehive to service users, such as
an introduction script, Beehive infographics, and other handouts.
Once programs started enrolling existing service users, many
found it difficult to transition enrolling new service users, given
that they already had numerous documentation requirements
during their clinical intake process. In response, we added a
“workflow meeting” to our training series where we asked
program leadership and key staff involved in intakes to walk
us through their existing procedures so that we could help
brainstorm where the required Beehive workflow steps could
be implemented and who from their program would be
responsible for each step. We additionally observed that
clinician-entered data were hard for sites to prioritize. For
example, there was a lack of clarity within teams about who
was responsible for entering these data and what training was
required. Therefore, we chose to add another “workflow
meeting” between key program staff and our team to help
programs identify who was responsible for which surveys, who
needed training, and how programs could monitor survey
completion. We added these workflow meetings to our formal
training protocol and made the support materials available to
all sites who joined after the piloting phase.
Furthermore, our team worked with programs beyond the
piloting phase to ensure that we continued to incorporate
individual feedback and offer continuous support, which is key
to successful adoption and can improve engagement [46]. After
the piloting of the beta version of Beehive concluded, we
continued to make development changes to meet users’ needs,
such as further design changes to the admin dashboard, widening
survey completion windows, adjusting and eventually allowing
customization of the frequency and timing of web link
notifications, allowing the EULA to be completed before survey
baseline date, simplifying registration fields, adding a survey
status page, adding additional survey visualizations, adding a
workflow for providers to enter data collected outside of
Beehive, and prioritizing the order of additional languages in
the app based on active need in the participating clinics. This
iterative approach in response to user feedback is consistent
with the development process of other eHealth apps [47].
This study highlights how critical it is for programs using a
continuous improvement approach, such as UCD, to budget
appropriately for ongoing development needs and staff time for
ongoing support. As long as an app is in use and collecting data
from real users, there should be a plan for ongoing project
management and app development to address feedback from
users, improve engagement and useability, and respond to
changing needs. Implementing UCD from the outset allowed
our team to be aware of and address user concerns before
investing valuable time and resources in initial development
and implementation. Focusing on workflow during the
storyboard and alpha phases of app and continuing this
collaborative relationship throughout the implementation phase
resulted in an app that represents the interests and needs of users.
During the piloting, we observed that survey completion rates
varied among different types of users. This variance may be
partially explained by our training approach during piloting (see
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 17https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 18 -->

the Results section). As we continue to collect data after the
piloting phase, we can evaluate if this trend continues beyond
the initial onboarding period throughout multiple years of data
collection. These varied results may also reflect the challenges
of implementing MBC, with or without an eHealth app, such
as the training burden and limited time to conduct new duties
associated with eHealth implementation [24-26,31]. When
implementing outcomes data collection in these settings, it may
be critical to gather only the minimum required data from EPI
program providers (eg, diagnosis) and rely on service-user
self-report measures whenever possible. Future analyses will
examine the relationship between characteristics of EPI program
providers (eg, degree and years licensed) and completion rates
of clinician-entered data. Future work, including barriers and
facilitators interviews with users after they gain more experience
using Beehive, will be used to prioritize the needs and
perspectives of our users in the ongoing development of Beehive
and to better understand the reasons why users do or do not
engage with the app [48].
Limitations
The COVID-19 pandemic introduced multiple challenges for
our study, which may have reduced the breadth and diversity
of participation in various phases of the project. We offered
workshops over remote teleconferencing instead of in-person,
which may have excluded individuals who are less comfortable
with using technology. This may have disproportionately
impacted on the recruitment of service users and support persons
for participation in workgroups, as our participant numbers were
lower than previous studies where we were conducting in-person
research [31]. To reduce bias that may have resulted from this
imbalance, we chose to prioritize the feedback of service users
and support persons if there was conflicting feedback between
these participants and EPI program provider participants. In
addition, the beta and full versions of Beehive have been
introduced to all service users in participating programs,
regardless of their comfort with technology, and this has allowed
us to incorporate informal feedback from these individuals as
we have continued to make improvements to Beehive.
Much of our data in UCD workshops were gathered at the start
of the COVID-19 pandemic, before anyone had experienced
the long-term shift in daily practices brought on by the increased
use of telehealth and remote working. We sought feedback on
an app that was intended for in-person use and received feedback
based on participants’ experience of using in-person services.
This highlights the importance of planning multiple
opportunities for soliciting and incorporating feedback from
sites so that apps can be responsive to changing environments.
Our workshops and piloting were only conducted in English.
To serve the diverse population of California, Beehive needs
to be both translated and adapted, a process known as
localization [49], into at least 15 languages. Since Beehive’s
launch, we have localized into 7 additional languages. We
continue to solicit feedback from users, including those whose
primary language is not English, to inform the ongoing
development of Beehive, and we will continue localize this app
into additional languages.
While we used our prior knowledge of mental health
development in the development of Beehive [11,12], we did
not use a structured analysis approach for the feedback obtained
during workshops due to time constraints imposed by project
deliverables. To reduce the impact of subjective biases, the
researchers who conducted each group debriefed afterward to
review the notes, and recordings were referenced if notes were
unclear or vague. In addition, all decisions about how to
incorporate feedback from these notes into app development
were made collaboratively by authors KEB, LMT, TAN, and
VLT. Future work in this area will benefit from organized
approaches to data collection and formal qualitative analysis
[50,51].
Conclusions
Working with community partners to co-design an eHealth app
for use in community EPI programs helped us to anticipate and
resolve barriers earlier in the app development and
implementation pipeline. On the basis of our observation and
the data, there appeared to be high levels of engagement with
Beehive. This resulted in feedback and continued design
improvements which allowed our team to be better poised to
launch Beehive across the EPI-CAL LHCN. Variance in survey
completion rates among respondent types suggests that support
persons and EPI program providers especially may need
additional support.
Acknowledgments
The authors would like to thank all service users, support persons, and EPI program providers who participated in this study,
Binda Mangat of Quorum Technologies, and its team of professionals for supporting the development of Beehive, and the Early
Psychosis Intervention Network of California learning health care network.
This research made was supported by One Mind, the National Institute of Mental Health under award R01MH120555-01, and
the following California counties: Los Angeles, Napa, Orange, San Diego, Solano, Stanislaus, Lake, Nevada, Mono, Colusa, and
Sonoma. The content is solely the responsibility of the authors and does not necessarily represent the official views of any sponsors
of the research.
Data Availability
The datasets generated and analyzed during this study are available from the corresponding author on reasonable request.
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 18https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 19 -->

Authors' Contributions
KEB conceptualized and designed the study, created the focus group guides, conceptualized and designed storyboards, recruited
participants, collected data, trained pilot sites, audited and cleaned data, analyzed data, drafted the manuscript, and reviewed and
revised the manuscript for important intellectual content. VLT conceptualized and designed the study, created the focus group
guides, conceptualized and designed storyboards, collected data, trained pilot sites, drafted the manuscript, and reviewed and
revised the manuscript for important intellectual content. KMP audited and cleaned data, drafted the manuscript, and reviewed
and revised the manuscript for important intellectual content. LMT conceptualized and designed the study, created the focus
group guides, conceptualized and designed storyboards, collected data, trained pilot sites, and reviewed and revised the manuscript
for important intellectual content. SE conceptualized and designed the study, created the focus group guides, collected data,
trained pilot sites, and reviewed and revised the manuscript for important intellectual content. MS, ABW, and AJP conceptualized
and designed the study and reviewed the manuscript for important intellectual content. LS collected data, trained pilot sites, and
reviewed and revised the manuscript for important intellectual content. CKH trained pilot sites, audited and cleaned data, and
reviewed and revised the manuscript for important intellectual content. VEP, APM, and MK-W trained pilot sites and reviewed
and revised the manuscript for important intellectual content. CM, MJM, NS, KLHN, and YZ cleaned data and reviewed and
revised the manuscript for important intellectual content. TAN obtained funding, conceptualized and designed the study, created
the focus group guides, conceptualized and designed storyboards, collected data, reviewed and revised the manuscript for important
intellectual content.
Conflicts of Interest
KEB consulted with ChatOwl Inc after data collection and before submission. LMT was employed by ChatOwl Inc, a digital
mental health company after data collection and before submission. LMT was a founder and owner of shares in Safari Health,
Inc. during project implementation, data collection, and write up (no longer true at time of writing) and is an employee and
shareholder at Kooth LLC at time of publication. TAN is a cofounder and shareholder in Safari Health, Inc.
Multimedia Appendix 1
The Early Psychosis Intervention Network of California outcomes collected in Beehive.
[DOCX File , 46 KB-Multimedia Appendix 1]
References
1. van Os J, Hanssen M, Bijl RV, Vollebergh W. Prevalence of psychotic disorder and community level of psychotic symptoms:
an urban-rural comparison. Arch Gen Psychiatry. Jul 2001;58(7):663-668. [doi: 10.1001/archpsyc.58.7.663] [Medline:
11448373]
2. Menchaca A, Pratt B, Jensen E, Jones N. Examining the racial and ethnic diversity of adults and children. United States
Census Bureau. May 22, 2023. URL: https://tinyurl.com/3wbpwc8t [accessed 2024-08-16]
3. Niendam TA, Sardo A, Savill M, Patel P, Xing G, Loewy RL, et al. The rise of early psychosis care in California: an
overview of community and university-based services. Psychiatr Serv. Jun 01, 2019;70(6):480-487. [doi:
10.1176/appi.ps.201800394] [Medline: 30890048]
4. Tryon VL, Nye KE, Savill M, Loewy R, Miles MJ, Tully LM, et al. The California collaborative network to promote data
driven care and improve outcomes in early psychosis (EPI-CAL) project: rationale, background, design and methodology.
BMC Psychiatry. Nov 14, 2024;24(1):800. [FREE Full text] [doi: 10.1186/s12888-024-06245-6] [Medline: 39543502]
5. Heinssen RK, Azrin ST. A national learning health experiment in early psychosis research and care. Psychiatr Serv. Sep
01, 2022;73(9):962-964. [FREE Full text] [doi: 10.1176/appi.ps.20220153] [Medline: 35895842]
6. Lewis CC, Boyd M, Puspitasari A, Navarro E, Howard J, Kassab H, et al. Implementing measurement-based care in
behavioral health: a review. JAMA Psychiatry. Mar 01, 2019;76(3):324-335. [FREE Full text] [doi:
10.1001/jamapsychiatry.2018.3329] [Medline: 30566197]
7. Firth J, Cotter J, Torous J, Bucci S, Firth JA, Yung AR. Mobile phone ownership and endorsement of "mHealth" among
people with psychosis: a meta-analysis of cross-sectional studies. Schizophr Bull. Mar 2016;42(2):448-455. [FREE Full
text] [doi: 10.1093/schbul/sbv132] [Medline: 26400871]
8. Naslund JA, Marsch LA, McHugo GJ, Bartels SJ. Emerging mHealth and eHealth interventions for serious mental illness:
a review of the literature. J Ment Health. 2015;24(5):321-332. [FREE Full text] [doi: 10.3109/09638237.2015.1019054]
[Medline: 26017625]
9. Meyer N, Kerz M, Folarin A, Joyce DW, Jackson R, Karr C, et al. Capturing rest-activity profiles in schizophrenia using
wearable and mobile technologies: development, implementation, feasibility, and acceptability of a remote monitoring
platform. JMIR Mhealth Uhealth. Oct 30, 2018;6(10):e188. [FREE Full text] [doi: 10.2196/mhealth.8292] [Medline:
30377146]
10. Torous J, Friedman R, Keshavan M. Smartphone ownership and interest in mobile applications to monitor symptoms of
mental health conditions. JMIR Mhealth Uhealth. Jan 21, 2014;2(1):e2. [FREE Full text] [doi: 10.2196/mhealth.2994]
[Medline: 25098314]
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 19https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 20 -->

11. Kumar D, Tully LM, Iosif AM, Zakskorn LN, Nye KE, Zia A, et al. A mobile health platform for clinical monitoring in
early psychosis: implementation in community-based outpatient early psychosis care. JMIR Ment Health. Feb 27,
2018;5(1):e15. [FREE Full text] [doi: 10.2196/mental.8551] [Medline: 29487044]
12. Niendam TA, Tully LM, Iosif AM, Kumar D, Nye KE, Denton JC, et al. Enhancing early psychosis treatment using
smartphone technology: a longitudinal feasibility and validity study. J Psychiatr Res. Jan 2018;96:239-246. [doi:
10.1016/j.jpsychires.2017.10.017] [Medline: 29126059]
13. Institute of Medicine, Committee on the Learning Health Care System in America, McGinnis JM, Stuckhardt L, Smith M,
Saunders R. Best Care at Lower Cost: The Path to Continuously Learning Health Care in America. Washington, DC.
National Academies Press; 2013.
14. Unützer J, Katon W, Callahan CM, Williams JWJ, Hunkeler E, Harpole L, et al. Collaborative care management of late-life
depression in the primary care setting: a randomized controlled trial. JAMA. Dec 11, 2002;288(22):2836-2845. [doi:
10.1001/jama.288.22.2836] [Medline: 12472325]
15. Katon WJ, Lin EH, Von Korff M, Ciechanowski P, Ludman EJ, Young B, et al. Collaborative care for patients with
depression and chronic illnesses. N Engl J Med. Dec 30, 2010;363(27):2611-2620. [FREE Full text] [doi:
10.1056/NEJMoa1003955] [Medline: 21190455]
16. Scott K, Lewis CC. Using measurement-based care to enhance any treatment. Cogn Behav Pract. Feb 2015;22(1):49-59.
[FREE Full text] [doi: 10.1016/j.cbpra.2014.01.010] [Medline: 27330267]
17. Heinssen RK, Goldstein AB, Azrin ST. Evidence-based treatments for first episode psychosis: components of coordinated
specialty care. National Institutes Mental Health. Apr 14, 2014. URL: https://www.nimh.nih.gov/sites/default/files/documents/
health/topics/schizophrenia/raise/evidence-based-treatments-for-first-episode-psychosis.pdf [accessed 2025-03-31]
18. Garland AF, Kruse M, Aarons GA. Clinicians and outcome measurement: what's the use? J Behav Health Serv Res.
2003;30(4):393-405. [doi: 10.1007/BF02287427] [Medline: 14593663]
19. Bickman L. A measurement feedback system (MFS) is necessary to improve mental health outcomes. J Am Acad Child
Adolesc Psychiatry. Oct 2008;47(10):1114-1119. [FREE Full text] [doi: 10.1097/CHI.0b013e3181825af8] [Medline:
20566188]
20. Trivedi MH, Daly EJ. Measurement-based care for refractory depression: a clinical decision support model for clinical
research and practice. Drug Alcohol Depend. May 2007;88 Suppl 2(Suppl 2):S61-S71. [FREE Full text] [doi:
10.1016/j.drugalcdep.2007.01.007] [Medline: 17320312]
21. Schreiweis B, Pobiruchin M, Strotbaum V, Suleder J, Wiesner M, Bergh B. Barriers and facilitators to the implementation
of eHealth services: systematic literature analysis. J Med Internet Res. Nov 22, 2019;21(11):e14197. [FREE Full text] [doi:
10.2196/14197] [Medline: 31755869]
22. Treisman GJ, Jayaram G, Margolis RL, Pearlson GD, Schmidt CW, Mihelish GL, et al. Perspectives on the use of eHealth
in the management of patients with schizophrenia. J Nerv Ment Dis. Aug 2016;204(8):620-629. [FREE Full text] [doi:
10.1097/NMD.0000000000000471] [Medline: 26828911]
23. Ossebaard HC, van Gemert-Pijnen L. eHealth and quality in health care: implementation time. Int J Qual Health Care. Jun
2016;28(3):415-419. [doi: 10.1093/intqhc/mzw032] [Medline: 27029590]
24. Hatfield DR, Ogles BM. Why some clinicians use outcome measures and others do not. Adm Policy Ment Health. May
2007;34(3):283-291. [doi: 10.1007/s10488-006-0110-y] [Medline: 17211715]
25. Zimmerman M, McGlinchey JB. Why don't psychiatrists use scales to measure outcome when treating depressed patients?
J Clin Psychiatry. Dec 2008;69(12):1916-1919. [doi: 10.4088/jcp.v69n1209] [Medline: 19192467]
26. Jensen-Doss A, Haimes EM, Smith AM, Lyon AR, Lewis CC, Stanick CF, et al. Monitoring treatment progress and providing
feedback is viewed favorably but rarely used in practice. Adm Policy Ment Health. Jan 2018;45(1):48-61. [FREE Full text]
[doi: 10.1007/s10488-016-0763-0] [Medline: 27631610]
27. Gould JD, Lewis C. Designing for usability: key principles and what designers think. Commun ACM. 1985;28(3):300-311.
[doi: 10.1145/3166.3170]
28. Norman DA, Draper SW. User Centered System Design: New Perspectives on Human-computer Interaction. Mahwah, NJ.
Lawrence Erlbaum Associates; 1986.
29. Gulliksen J, Göransson B, Boivie I, Blomkvist S, Persson J, Cajander Å. Key principles for user-centred systems design.
Behav Inform Technol. Nov 2003;22(6):397-409. [doi: 10.1080/01449290310001624329]
30. van Gemert-Pijnen JE, Nijland N, van Limburg M, Ossebaard HC, Kelders SM, Eysenbach G, et al. A holistic framework
to improve the uptake and impact of eHealth technologies. J Med Internet Res. Dec 05, 2011;13(4):e111. [FREE Full text]
[doi: 10.2196/jmir.1672] [Medline: 22155738]
31. Savill M, Banks LM, Tryon VL, Ereshefsky S, Nye KE, Botello RM, et al. Exploring data collection priorities of community
partners in early psychosis care. Psychiatr Serv. Sep 01, 2024;75(9):854-862. [doi: 10.1176/appi.ps.20230455] [Medline:
38595117]
32. Tully LM, Nye KE, Ereshefsky S, Tryon VL, Hakusui CK, Savill M, et al. Incorporating community partner perspectives
on eHealth technology data sharing practices for the California early psychosis intervention network: qualitative focus
group study with a user-centered design approach. JMIR Hum Factors. Nov 14, 2023;10:e44194. [FREE Full text] [doi:
10.2196/44194] [Medline: 37962921]
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 20https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 21 -->

33. Endmann A, Keßner D. User journey mapping – a method in user experience design. i-com. 2016;15(1):105-110. [doi:
10.1515/icom-2016-0010]
34. Newman MW, Landay JA. Sitemaps, storyboards, and specifications: a sketch of Web site design practice. In: Proceedings
of the 3rd Conference on Designing Interactive Systems: Processes, Practices, Methods, and Techniques. 2000. Presented
at: DIS '00; August 17-19, 2000; New York, NY. [doi: 10.1145/347642.347758]
35. Ludden GD, van Rompay TJ, Kelders SM, van Gemert-Pijnen JE. How to increase reach and adherence of web-based
interventions: a design research viewpoint. J Med Internet Res. Jul 10, 2015;17(7):e172. [FREE Full text] [doi:
10.2196/jmir.4201] [Medline: 26163456]
36. Core Assessment Battery (CAB). Early Psychosis Intervention Network. URL: https://nationalepinet.org/
core-assessment-battery-cab/ [accessed 2024-08-16]
37. Boothroyd RA, Chen HJ. The psychometric properties of the Colorado Symptom Index. Adm Policy Ment Health. Sep
2008;35(5):370-378. [doi: 10.1007/s10488-008-0179-6] [Medline: 18561020]
38. de Beurs D, van Bruinessen I, Noordman J, Friele R, van Dulmen S. Active involvement of end users when developing
web-based mental health interventions. Front Psychiatry. 2017;8:72. [FREE Full text] [doi: 10.3389/fpsyt.2017.00072]
[Medline: 28515699]
39. van Bruinessen IR, van Weel-Baumgarten EM, Snippe HW, Gouw H, Zijlstra JM, van Dulmen S. Active patient participation
in the development of an online intervention. JMIR Res Protoc. Nov 06, 2014;3(4):e59. [FREE Full text] [doi:
10.2196/resprot.3695] [Medline: 25379679]
40. van Hierden Y, Dietrich T, Rundle-Thiele S. Designing an eHealth well-being program: a participatory design approach.
Int J Environ Res Public Health. Jul 06, 2021;18(14):7250. [FREE Full text] [doi: 10.3390/ijerph18147250] [Medline:
34299700]
41. Honary M, Fisher NR, McNaney R, Lobban F. A web-based intervention for relatives of people experiencing psychosis or
bipolar disorder: design study using a user-centered approach. JMIR Ment Health. Dec 07, 2018;5(4):e11473. [FREE Full
text] [doi: 10.2196/11473] [Medline: 30530457]
42. Mak C, Whittingham K, Cunnington R, Boyd RN. Efficacy of mindfulness-based interventions for attention and executive
function in children and adolescents—a systematic review. Mindfulness. Jul 26, 2017;9(1):59-78. [doi:
10.1007/s12671-017-0770-6]
43. Kajitani K, Higashijima I, Kaneko K, Matsushita T, Fukumori H, Kim D. Short-term effect of a smartphone application
on the mental health of university students: a pilot study using a user-centered design self-monitoring application for mental
health. PLoS One. 2020;15(9):e0239592. [FREE Full text] [doi: 10.1371/journal.pone.0239592] [Medline: 32976515]
44. Bakker D, Kazantzis N, Rickwood D, Rickard N. Mental health smartphone apps: review and evidence-based
recommendations for future developments. JMIR Ment Health. Mar 01, 2016;3(1):e7. [FREE Full text] [doi:
10.2196/mental.4984] [Medline: 26932350]
45. The value of beehive. YouTube. URL: https://www.youtube.com/watch?v=-7MDPRLU1BM&feature=youtu.be [accessed
2024-08-29]
46. Glomann L, Hager V, Lukas CA, Berking M. Patient-centered design of an e-mental health app. In: Joint Proceedings of
the AHFE 2018 International Conference on Human Factors in Artificial Intelligence and Social Computing, Software and
Systems Engineering, The Human Side of Service Engineering and Human Factors in Energy. 2018. Presented at: AHFE
2018; July 21-25, 2018; Orlando, FL. [doi: 10.1007/978-3-319-94229-2_25]
47. Kip H, Keizer J, da Silva MC, Beerlage-de Jong N, Köhle N, Kelders SM. Methods for human-centered eHealth development:
narrative scoping review. J Med Internet Res. Jan 27, 2022;24(1):e31858. [FREE Full text] [doi: 10.2196/31858] [Medline:
35084359]
48. Ereshefsky S, Gemignani R, Savill M, Sanford KC, Banks LM, Tryon VL, et al. A mixed-methods study exploring the
benefits, drawbacks, and utilization of data in care: findings from the EPI-CAL early psychosis learning health care network.
Schizophr Res. Feb 2025;276:157-166. [FREE Full text] [doi: 10.1016/j.schres.2025.01.018] [Medline: 39892249]
49. Schäler R. Localization and translation. In: Handbook of Translation Studies Online. Amsterdam, The Netherlands. John
Benjamins Publishing Company; 2010:209-214.
50. Molina-Recio G, Molina-Luque R, Jiménez-García AM, Ventura-Puertos PE, Hernández-Reyes A, Romero-Saldaña M.
Proposal for the user-centered design approach for health apps based on successful experiences: integrative review. JMIR
Mhealth Uhealth. Apr 22, 2020;8(4):e14376. [FREE Full text] [doi: 10.2196/14376] [Medline: 32319965]
51. Ozkaynak M, Sircar CM, Frye O, Valdez RS. A systematic review of design workshops for health information technologies.
Informatics. May 14, 2021;8(2):34. [doi: 10.3390/informatics8020034]
Abbreviations
EPI: early psychosis intervention
EPI-CAL: Early Psychosis Intervention Network of California
EULA: end user license agreement
HIPAA: Health Insurance Portability and Accountability Act
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 21https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX

<!-- Page 22 -->

LHCN: learning health care network
MBC: measurement-based care
MCSI: Modified Colorado Symptom Index
UCD: user-centered design
Edited by C Jacob; submitted 04.11.24; peer-reviewed by J D'Arcey; comments to author 06.12.24; revised version received 19.12.24;
accepted 12.03.25; published 09.04.25
Please cite as:
Burch KE, Tryon VL, Pierce KM, Tully LM, Ereshefsky S, Savill M, Smith L, Wilcox AB, Hakusui CK, Padilla VE, McNamara AP,
Kado-Walton M, Padovani AJ, Miller C, Miles MJ, Sharma N, Nguyen KLH, Zhang Y, Niendam TA
Co-Designing a Web-Based and Tablet App to Evaluate Clinical Outcomes of Early Psychosis Service Users in a Learning Health
Care Network: User-Centered Design Workshop and Pilot Study
JMIR Hum Factors 2025;12:e65889
URL: https://humanfactors.jmir.org/2025/1/e65889
doi: 10.2196/65889
PMID:
©Kathleen E Burch, Valerie L Tryon, Katherine M Pierce, Laura M Tully, Sabrina Ereshefsky, Mark Savill, Leigh Smith, Adam
B Wilcox, Christopher Komei Hakusui, Viviana E Padilla, Amanda P McNamara, Merissa Kado-Walton, Andrew J Padovani,
Chelyah Miller, Madison J Miles, Nitasha Sharma, Khanh Linh H Nguyen, Yi Zhang, Tara A Niendam. Originally published in
JMIR Human Factors (https://humanfactors.jmir.org), 09.04.2025. This is an open-access article distributed under the terms of
the Creative Commons Attribution License (https://creativecommons.org/licenses/by/4.0/), which permits unrestricted use,
distribution, and reproduction in any medium, provided the original work, first published in JMIR Human Factors, is properly
cited. The complete bibliographic information, a link to the original publication on https://humanfactors.jmir.org, as well as this
copyright and license information must be included.
JMIR Hum Factors 2025 | vol. 12 | e65889 | p. 22https://humanfactors.jmir.org/2025/1/e65889
(page number not for citation purposes)
Burch et alJMIR HUMAN FACTORS
XSL•FO
RenderX