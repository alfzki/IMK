# information-17-00606-v2


<!-- Page 1 -->

Academic Editor: Aneta
Poniszewska-Maranda
Received: 4 May 2026
Revised: 5 June 2026
Accepted: 13 June 2026
Published: 17 June 2026
Copyright: © 2026 by the authors.
Licensee MDPI, Basel, Switzerland.
This article is an open access article
distributed under the terms and
conditions of the Creative Commons
Attribution (CC BY) license.
Article
A Multimethod Framework for Evaluating Institutional Website
Usability: Integrating Kano, WebQual 4.0, QFD and
Heuristic Analysis
Daniel Raposo 1,2
 , Fátima Veríssimo 2, Teresa Paiva 3,4, *
 , João Neves 1,2 and Teresa Felgueira 5
1 ReThink—Centro de Investigação em Design para o Território & Polytechnic Institute of Castelo Branco,
6000-084 Castelo Branco, Portugal; draposo@ipcb.pt (D.R.); joaoneves@ipcb.pt (J.N.)
2 CIAUD—Centro de Investigação em Arquitetura, Urbanismo e Design, Lisbon School of Architecture,
Universidade de Lisboa, 1349-063 Lisboa, Portugal; fatima_verissimo@ipcb.pt
3 BRIDGES—Biotechnology Research, Innovation and Design for Health Products, Polytechnic Institute of
Guarda, 6300-559 Guarda, Portugal
4 NECE—Research Centre in Business Sciences, University of Beira Interior, 6200-209 Covilhã, Portugal
5 CITUR—Centre for Tourism Research, Development and Innovation, School of Technology and Management,
Polytechnic Institute of Guarda, 6300-559 Guarda, Portugal; tfelgueira@ipg.pt
* Correspondence: tpaiva@ipg.pt
Abstract
This study proposes a structured, replicable, multimethod framework for evaluating the us-
ability of institutional information systems serving heterogeneous user groups. It addresses
the limited integration of expectation–satisfaction analysis, perception-based quality as-
sessment, and technical prioritisation by combining the Kano Model, WebQual 4.0, Quality
Function Deployment (QFD), and heuristic evaluation within a unified workflow. The
framework was applied to the Interior+ platform through a user survey (n = 40) and an
expert heuristic inspection (n = 4). Results indicate that usability, responsiveness, and infor-
mation clarity serve as basic (must-be) attributes, leading to high potential for dissatisfaction
when performance is inadequate. In contrast, multimedia content and personalisation
emerged as attractive attributes that enhance satisfaction without generating substantial
dissatisfaction when absent. The integration of Kano, WebQual, and QFD enabled the sys-
tematic prioritisation of technical improvements, while comparison with expert evaluations
revealed an 80% convergence between user-derived priorities and heuristic recommen-
dations. The findings also highlight meaningful divergences between users and experts,
particularly regarding information clarity, reinforcing the value of triangulated evaluation
approaches. The study contributes a practical, operationalised protocol that integrates
user perceptions, expert assessments, and decision-support tools to inform evidence-based
usability improvements and the development of more inclusive, effective, and user-centred
institutional digital platforms.
Keywords: usability evaluation; Kano Model; WebQual 4.0; Quality Function Deployment
(QFD); User Experience Design (UXD); heuristic evaluation; digital inclusion; user-centred
design
1. Introduction
The quality and usability of institutional websites have become central to the effec-
tiveness of digital public services and the promotion of digital inclusion. As governments
and organisations increasingly rely on online platforms to communicate with citizens and
Information 2026, 17, 606 https://doi.org/10.3390/info17060606

<!-- Page 2 -->

Information 2026, 17, 606 2 of 33
deliver services, the performance of these digital interfaces directly affects access to informa-
tion, participation in public initiatives, and the overall perception of institutional credibility.
In particular, platforms dedicated to territorial management and regional development
must address complex challenges related to heterogeneous user profiles, varying levels of
digital literacy, and the need to communicate information clearly and accessibly [1–3].
In this context, a substantial body of research has focused on evaluating website quality
and its relationship to user satisfaction. Studies examining digital government portals and
institutional platforms consistently demonstrate that user satisfaction depends not only
on the availability of services but also on the perceived quality of information, usability
of the interface, and effectiveness of interaction mechanisms [4–6]. Among the evaluation
frameworks proposed in the literature, the WebQual 4.0 model has become one of the most
widely adopted instruments for measuring perceived website quality, particularly due to
its ability to translate subjective user perceptions into structured analytical dimensions.
Complementary research has examined how specific attributes of digital platforms
influence user satisfaction. Previous studies highlight that website quality dimensions, par-
ticularly usability, information quality and service interaction, play a central role in shaping
user perceptions and satisfaction with online services. Reliable and accessible information
is therefore critical to ensuring the effectiveness of digital platforms, especially in contexts
where users depend on online systems for information and access to services [7,8]. For
example, Leite et al. [9] emphasise that the reliability and accessibility of online information
are essential factors when evaluating the effectiveness of institutional digital platforms,
particularly in contexts where citizens rely on online resources for decision-making and
access to services. These findings reinforce the importance of combining perceptual evalua-
tion models with structured decision-support methods that translate user expectations into
actionable design improvements.
Empirical studies using models such as the End-User Computing Satisfaction
(EUCS) model show that dimensions such as content quality, information accuracy, in-
terface clarity, and ease of navigation significantly affect users’ evaluations of digital
platforms [10–12]. These findings suggest that user satisfaction arises from a multidimen-
sional interplay among system functionality, information quality, and the experiential
aspects of digital interaction.
Despite the extensive use of such evaluation frameworks, several authors highlight
important limitations in existing approaches. In many cases, traditional website evaluation
models focus primarily on measuring perceived quality, without offering mechanisms to
identify the relative importance of specific attributes or to translate user perceptions into
actionable design priorities [ 13,14]. Consequently, organisations may obtain diagnostic
insights about user perceptions but still lack structured tools to guide the prioritisation of
technical improvements.
To address this limitation, several studies propose integrating perceptual evaluation
models with decision-support methodologies that operationalise the “voice of the user”.
In this regard, the Kano Model has emerged as an important framework for identifying
how different attributes influence satisfaction and dissatisfaction. Unlike traditional linear
approaches to service quality, the Kano model recognises that user satisfaction is influenced
by heterogeneous categories of attributes, including essential requirements, performance
factors and attractive features that may unexpectedly enhance the user experience.
When combined with technical prioritisation frameworks such as Quality Function De-
ployment (QFD), the Kano model enables organisations to translate user expectations into
structured design requirements. This integration has been successfully applied in several
domains, including financial services, product design, and industrial engineering, where it
has proven effective in aligning user needs with technical development processes [15–23].
https://doi.org/10.3390/info17060606

<!-- Page 3 -->

Information 2026, 17, 606 3 of 33
However, despite its potential, the application of this integrated methodological framework
remains relatively limited in digital public services and institutional platforms.
Another dimension that has received increasing attention in recent years concerns the
divergence between user evaluations and those conducted by usability experts. Research
on human–computer interaction indicates that users typically identify practical obstacles
related to navigation, information clarity, and task completion, whereas expert evaluators
tend to detect structural usability issues, heuristic inconsistencies, and interface design
flaws [24–26]. This divergence reflects different evaluation paradigms and highlights the
importance of combining participatory and expert-driven assessment methods.
In the public sector, such methodological complementarity is particularly relevant.
Participatory approaches emphasise the role of citizens as co-producers of public services,
while expert evaluation contributes technical rigour and methodological consistency in
identifying design limitations [27–30]. Nevertheless, empirical studies comparing these
two perspectives remain scarce, especially in digital platforms dedicated to territorial
development and regional revitalisation.
Against this background, the present study addresses two interrelated gaps in the
literature. First, it addresses the need for integrated methodological approaches that
link perceptual quality evaluation to structured prioritisation of technical improvements.
Second, it contributes to the limited empirical evidence comparing user-centred evaluation
with expert-based usability inspection in institutional digital platforms.
To this end, the study proposes the integrated application of three complementary
methods, WebQual 4.0, the Kano Model and Quality Function Deployment (QFD), com-
bined with a heuristic expert evaluation of the Interior+ website, an institutional platform
designed to support the revitalisation of rural communities. Rather than focusing on
the novelty of each method individually, the study’s contribution lies in the operational
integration of these approaches, enabling a systematic connection among user perceptions,
quality prioritisation, and technical recommendations, while also allowing a comparative
analysis between user-based and expert-based evaluations.
Based on the theoretical framework and the identified gaps, the following research
questions and working hypotheses are formulated:
RQ1. How do different attributes of usability and quality of information influence user satisfaction
and dissatisfaction?
RQ2. How does the Kano–WebQual–QFD integration contribute to a consistent technical prioriti-
sation against the heuristic evaluation of the experts?
RQ3. To what extent do the problems identified by users differ from those identified by experts, and
what are the implications of this divergence?
To guide the study, the following testable hypotheses are formulated:
H1a. Essential attributes such as usability, responsiveness and information clarity are associated
with higher dissatisfaction when absent.
H1b. The integrated process (Kano—WebQual—QFD) generates a prioritisation of requirements
that is consistent with at least 70% of the critical recommendations identified by the experts.
H1c. There are statistically significant differences between the problems identified by users and
experts, reflecting different evaluation paradigms. These hypotheses guide the analysis and provide
the basis for the discussion on methodological complementarity.
https://doi.org/10.3390/info17060606

<!-- Page 4 -->

Information 2026, 17, 606 4 of 33
The contributions are tripartite: (i) we propose a replicable, documented protocol appli-
cable to institutional websites; (ii) we present empirical evidence on how different attributes
influence satisfaction and technical priorities; (iii) we provide a comparative analysis be-
tween user assessment and expert inspection, highlighting complementarities and practical
implications for the design of digital platforms oriented towards territorial inclusion.
2. Theoretical Background
The evaluation of digital service quality has evolved significantly over the past three
decades, reflecting the growing complexity of online interactions and the increasing cen-
trality of digital platforms in organisational communication and service delivery. Early
conceptualisations of service quality, particularly the SERVQUAL model proposed by
Parasuraman, Zeithaml and Berry [31], provided the theoretical foundation for analysing
user perceptions of service performance by measuring the gap between expectations and
perceived outcomes. Although originally developed for face-to-face service environments,
SERVQUAL strongly influenced subsequent models designed for digital contexts. As
digital services expanded, researchers adapted these principles to account for character-
istics specific to online environments, including system availability, interface usability,
information quality and responsiveness [ 32]. These adaptations gave rise to a series of
specialised frameworks for evaluating the quality of digital platforms and their impact on
user satisfaction.
Within the field of information systems, several empirical studies have confirmed that
perceived quality of digital services is a critical determinant of user satisfaction, trust and
continued use intention. Research across institutional websites, e-government platforms,
and organisational portals consistently identifies usability, information reliability, and
interaction quality as central determinants of positive user experiences [ 4,11,33]. These
findings highlight the need for analytical models capable of capturing both technical system
characteristics and subjective user perceptions.
Among the various frameworks proposed for this purpose, WebQual 4.0 stands out
as one of the most widely adopted models for evaluating website quality from the user
perspective. Developed by Barnes and Vidgen [34], the model operationalises the evaluation
of websites through three core dimensions: usability, information quality and interaction
quality. By structuring subjective perceptions into measurable indicators, WebQual enables
researchers and practitioners to analyse the digital user experience systematically.
However, assessing usability on digital platforms requires approaches that transcend
purely functional and technical aspects. It is also necessary to consider emotional, social
and contextual factors that shape digital interaction. In this sense, the Generalised User
Experience Questionnaire (UEQ-G), developed by Boothe et al. [35] is an effective tool for
capturing multimodal experiences by integrating both pragmatic and hedonic qualities in
product and service contexts.
In a convergent perspective, research on digital platforms highlights that user expe-
rience should extend beyond functional efficiency and incorporate experiential and per-
ceptual dimensions that influence users’ engagement with the interface. Studies analysing
website quality and user experience indicate that attributes such as usability, information
clarity and interaction quality significantly shape users’ perceptions and satisfaction with
digital systems [ 12,35,36]. These findings suggest that successful digital platforms are
those that not only operate effectively but also create meaningful, engaging experiences,
strengthening users’ connection to the interface and enhancing overall satisfaction.
The choice of the evaluation instrument directly impacts the results obtained.
Schrepp et al. [37] compared the SUS, UMUX-LITE, and UEQ-S questionnaires, demon-
strating that although SUS and UMUX-LITE perform similarly in measuring usability,
https://doi.org/10.3390/info17060606

<!-- Page 5 -->

Information 2026, 17, 606 5 of 33
UEQ-S is distinguished by its ability to capture the hedonic dimension, which is essential
for a more holistic understanding of the user experience.
Accessibility is a fundamental dimension of digital quality, particularly on in-
stitutional and public digital platforms, where inclusivity is a central requirement.
Koutsabasis et al. [38] proposed a practical methodology for evaluating web accessibil-
ity that goes beyond technical compliance with accessibility standards. Their approach
emphasises identifying specific user requirements, defining explicit accessibility objectives,
and implementing continuous monitoring mechanisms. This perspective highlights that
accessibility should be integrated from the earliest stages of system design rather than
treated as a post-development adjustment. Similarly, user-centred design approaches em-
phasise that website quality depends on the ability to accommodate diverse user needs and
capabilities, reinforcing the importance of inclusive usability in digital service design.
The integration of qualitative and quantitative methods is also productive for identify-
ing usability problems. Alhadreti and Mayhew [39] concluded that, when comparing the
traditional and co-participatory think-aloud methods, the latter allows for the identification
of more problems, especially those of lesser severity, thus offering more detailed insights
for the continuous improvement of the interface.
In addition, Moon et al. [ 40] highlight the role of empathetic design in developing
inclusive digital solutions. In a study on the prototyping of interactive visualisations
for health services, the authors show how co-creation with users, anchored in empathy,
allows the identification of hidden barriers and generates innovative responses with high
social impact.
The convergence of these frameworks, perceptual analysis models, holistic measure-
ment tools, and participatory methodologies enables a multidimensional reading of the
user experience. This approach underpins design as an evidence-driven practice, capable
of translating perceptions into informed strategic decisions, thereby promoting accessibility,
inclusion, and greater communicative effectiveness in digital environments.
2.1. Quality of Service and Digital Usability
Evaluating the quality of digital services requires analytical frameworks that capture
the complexity of interactions between users and online interfaces. Unlike traditional ser-
vice environments, digital platforms combine technical system performance with cognitive,
behavioural and perceptual aspects of user interaction. As a result, the assessment of digital
usability must consider not only functional efficiency but also the clarity of information,
accessibility of services, and users’ confidence when navigating the system.
Research in information systems consistently demonstrates that usability is one of
the most influential determinants of user satisfaction and continued engagement with
digital platforms. Empirical studies of institutional websites, e-government services, and
organisational portals indicate that users tend to prioritise intuitive navigation structures,
clear information architecture, and efficient task-completion mechanisms when evaluating
online experiences [4,11]. When these elements are absent or poorly implemented, users
often experience frustration, leading to lower satisfaction levels and reduced trust in the
digital service.
In response to these challenges, several authors have proposed heuristic and indicator-
based approaches to guide the evaluation of website quality. One example is the checklist
developed by Veríssimo et al. [41], which proposes a structured matrix of 108 indicators or-
ganised across four dimensions: content, design, navigation and educational functionalities.
The framework integrates classic usability principles, such as Nielsen’s [42] heuristics of
consistency, error prevention and informative feedback, with contemporary digital quality
models, including WebQEM [42,43], SiteQual [44] and WebQual [45].
https://doi.org/10.3390/info17060606

<!-- Page 6 -->

Information 2026, 17, 606 6 of 33
The indicators included in this checklist encompass criteria such as the accuracy
and updating of information, readability, visual hierarchy, accessibility, interactivity and
institutional transparency. Applied to a sample of higher education institution websites, the
tool demonstrated its capacity to identify structural and functional weaknesses in digital
interfaces, thereby supporting targeted improvement initiatives [41]. At the same time, the
authors acknowledge that heuristic evaluations alone cannot fully capture the diversity
of user experiences, emphasising the need to complement expert-based assessments with
empirical user data.
This limitation reflects a broader challenge in digital usability research. While heuristic
evaluation methods are effective in diagnosing structural design issues, they do not neces-
sarily reveal how users perceive the relative importance of different attributes or how these
attributes influence satisfaction. Consequently, many scholars advocate combining expert-
based diagnostic tools with user-centred evaluation models that capture the experiential
dimensions of digital interaction.
In this sense, usability evaluation increasingly relies on multimethod approaches that
integrate heuristic inspection, user perception surveys and behavioural analysis. Such
methodological triangulation allows researchers to move beyond purely technical assess-
ments and develop a more comprehensive understanding of how design choices influence
user satisfaction and engagement.
Quality assessment in digital environments requires models capable of capturing
the complexity of interactions between users and interfaces. Online experiences involve
not only functional efficiency but also subjective factors such as information clarity, ac-
cessibility, and confidence in navigation. In this context, evaluation instruments based
on heuristics and observational criteria become valuable tools for both diagnosing and
guiding improvements in institutional websites.
The checklist developed by Veríssimo et al. [41] exemplifies this approach, proposing
a matrix of 108 indicators distributed across four major dimensions: content, design, navi-
gation, and educational functionalities. The proposal integrates classic heuristic principles,
such as those of Nielsen [42], which include consistency, error prevention and informative
feedback, with contemporary digital quality references, such as WebQEM [43], SiteQual [44]
and WebQual [45]. These indicators cover criteria such as updating and accuracy of infor-
mation, credibility, readability, visual hierarchy, usability, accessibility, interactivity, and
institutional adequacy. The checklist also includes specific elements of educational institu-
tions’ websites, such as the presentation of the training offer, information on admissions,
student services, and internationalisation resources. When applied to a sample of six
websites of higher education institutions, the tool proved effective in identifying gaps and
supporting improvements to the digital experience. However, the authors acknowledge
that their validation remains partial and recommend future applications involving real
users to reinforce the proposal’s robustness [41].
More than an evaluative instrument, this checklist assumes a formative role, offering a
structured basis for the development and continuous improvement of digital platforms
with an educational or institutional mission. Its use is particularly relevant in contexts that
require clear communication, technical accessibility, and strengthened user trust, such as
university websites, public services, and digital social projects, including Interior+.
2.2. WebQual 4.0 Model: Perceptual and Heuristic Assessment
Among the frameworks developed to evaluate website quality from the user per-
spective, the WebQual 4.0 model stands out as one of the most widely applied in digital
service research. Proposed by Barnes and Vidgen [34], WebQual adapts the principles of the
https://doi.org/10.3390/info17060606

<!-- Page 7 -->

Information 2026, 17, 606 7 of 33
SERVQUAL model to online environments, offering a structured approach to measuring
perceived website quality.
The model conceptualises website quality through the following three core dimensions.
• Usability: includes Criteria such as intuitive navigation, ease of learning, and efficiency
in use.
• Information Quality: Covers the accuracy , relevance, timeliness and clarity ofthe contents.
• Interaction Quality: This refers to the trust, customisation, support, and responsiveness
of the interface.
This tripartite structure reflects the multidimensional nature of digital interaction,
recognising that users evaluate online platforms not only on their technical functionality
but also on the quality and credibility of the information they provide and the perceived
reliability of the service.
By relying on subjective perceptions, WebQual enables user-driven heuristic evalu-
ation and is especially useful in contexts where the individual and emotional experience
of digital browsing is central. The structure of the model facilitates the conversion of
qualitative judgments into analysable data, promoting a bridge between the empirical
domain of user experience and the functional requirements of digital design.
Empirical applications of WebQual across various domains, including e-government
portals, university websites and online services, demonstrate that these three dimensions
consistently explain a significant portion of variance in user satisfaction and perceived
service quality [4,5]. In particular, usability and information quality frequently emerge as
the most influential factors shaping user evaluations of institutional websites.
Despite its robustness as a perceptual evaluation tool, WebQual has certain limitations.
While it effectively captures users’ subjective perceptions of digital quality, it does not inher-
ently provide mechanisms for identifying latent expectations or prioritising improvement
actions. In other words, the model is highly effective in diagnosing perceived quality gaps
but less suited for determining which attributes should be prioritised in system redesign.
For this reason, several researchers have proposed combining WebQual with comple-
mentary analytical frameworks to identify hidden user needs and translate perceptual data
into strategic design decisions. One such framework is the Kano model, which introduces
a nonlinear perspective on the relationship between service attributes and user satisfaction.
Studies, such as that of Hidayat et al. [ 46], demonstrate the potential of combining
WebQual with other models, such as Kano, to identify latent or unspoken needs, as-
pects that often escape purely technical models but are fundamental to the overall degree
of satisfaction.
By comparison, the checklist by Veríssimo et al. [41] presents a more extensive and
contextualised structure, covering emotional, institutional, and aesthetic criteria that are
not explored to the same depth in WebQual. If Barnes and Vidgen’s model [ 34] offers
a functional and synthetic reading of the digital experience, the checklist serves as a
complementary tool, enabling more specific and refined diagnoses. This complementarity
becomes particularly relevant when it is intended to feed translation models such as QFD,
which require accurate qualitative data to guide design decisions.
2.3. Kano Model: Capturing the Level of Satisfaction with Nonlinear Sensitivity
The Kano model, originally proposed by Noriaki Kano [ 47], and later developed
by several authors [48,49] represents a significant conceptual advance in the analysis of
customer satisfaction by challenging the traditional assumption that improvements in
product or service performance generate proportional increases in satisfaction. Instead, the
model argues that different attributes influence user perceptions in distinct ways.
The model classifies attributes into the following four main categories.
https://doi.org/10.3390/info17060606

<!-- Page 8 -->

Information 2026, 17, 606 8 of 33
• Must-be attributes: These are expected by users; their absence generates a strong level
of frustration, but their presence is taken for granted.
• Performance attributes (one-dimensional): The better executed, the higher the degree
of satisfaction.
• Attractive attributes: They surprise positively; they are not expected, but delight
when present.
• Indifferent or reverse attributes: They do not significantly affect the experience or lead
to harm when misapplied.
This categorisation introduces a nonlinear understanding of satisfaction, enabling
researchers to distinguish between essential requirements and potential sources of differen-
tiation. Subsequent developments of the Kano model incorporate quantitative measures
such as the Satisfaction Index (SI) and Dissatisfaction Index (DI), which allow researchers
to estimate the relative impact of each attribute on overall user perception. In this study,
this extended operationalisation, combining the original categorical structure with SI/DI
indices, is referred to as the “Kano model with quantitative extension” or simply the Kano
model throughout, in line with standard academic usage.
In the context of digital platforms, the Kano model has proven particularly useful for
identifying latent expectations that may not be captured by traditional usability metrics.
Studies applying Kano to website design and digital service evaluation demonstrate that
attributes related to navigation efficiency, responsiveness and information clarity often
function as must-be factors, while elements such as personalisation features or advanced
multimedia content tend to operate as attractive attributes [46–50].
By distinguishing between different categories of user expectations, the Kano model
provides valuable insights into how design improvements should be prioritised. However,
while the model effectively identifies the relative importance of attributes from the user
perspective, it does not directly translate these insights into concrete technical specifica-
tions. This limitation highlights the need for complementary methodologies capable of
operationalising the “voice of the user” within the design process.
2.4. QFD: Strategic Operationalisation of User Voice
Quality Function Deployment (QFD), developed by Akao [ 51] addresses this chal-
lenge by providing a systematic methodology for translating user needs into technical
requirements. The core objective of QFD is to ensure that design decisions are directly
aligned with user expectations, thereby improving the effectiveness of product and service
development processes.
The central analytical tool in QFD is the House of Quality, a matrix that links cus-
tomer requirements to the system’s technical characteristics. By establishing correlations
between these elements, the matrix allows designers and decision-makers to evaluate the
relative importance of different requirements, identify potential conflicts between design
parameters and prioritise improvement actions.
In the context of digital services, QFD plays a crucial role in bridging the gap between
qualitative user insights and technical implementation strategies. While perceptual models
such as WebQual and Kano provide valuable information about how users experience
digital platforms, QFD translates these insights into structured development priorities.
The integration of QFD with user-centred evaluation models has been widely docu-
mented in the literature. Studies combining Kano and QFD demonstrate that this method-
ological articulation significantly improves the alignment between user expectations and
system design decisions [15,52,53]. By incorporating satisfaction and dissatisfaction indices
derived from the Kano model into the QFD matrix, organisations can prioritise technical
improvements based on both user impact and implementation feasibility.
https://doi.org/10.3390/info17060606

<!-- Page 9 -->

Information 2026, 17, 606 9 of 33
This approach is particularly valuable in complex digital environments where multiple
stakeholders, resource constraints and strategic objectives must be balanced. Through the
systematic translation of user perceptions into operational design parameters, QFD enables
a structured and transparent decision-making process that enhances the effectiveness of
digital platform development.
When used in conjunction with perceptual models such as Kano and WebQual 4.0,
QFD not only organises the diagnosis but also leads to informed and strategic prioritisation,
resulting in a more functional and user-centred design, aligning technical decisions with
the values and expectations of the various target audiences.
2.5. Comparison and Convergence: Integration of the Three Models
The evaluation and improvement of digital platforms require analytical approaches
that capture not only how users perceive website quality but also how these perceptions
translate into actionable design priorities. Individually, WebQual, the Kano Model and
Quality Function Deployment (QFD) provide valuable but partial perspectives on this
challenge. The integration of the Kano, WebQual 4.0 and QFD models constitutes more than
a methodological juxtaposition: it represents a coherent chain of sensitive diagnosis, evalu-
ative structure and strategic decision. Each model assumes a distinct and complementary
role within a systematic process of evaluating and improving the digital experience.
The Kano Model complements this limitation by introducing an asymmetric perspec-
tive on user satisfaction. Rather than assuming a linear relationship between performance
and satisfaction, the model recognises that different attributes exert distinct effects on user
perceptions [47–49]. Basic requirements may generate dissatisfaction when absent, without
necessarily increasing satisfaction when present, whereas attractive features can create
positive experiences even when not explicitly expected by users [47,48]. The incorporation
of Satisfaction Index (SI) and Dissatisfaction Index (DI) coefficients further enables the
quantitative estimation of each attribute’s contribution to overall user experience [48,49].
WebQual provides a structured mechanism for measuring perceived website quality
through the dimensions of usability, information quality and interaction quality [34]. These
dimensions capture how users experience the website and identify areas where perceptions
of quality may be weakened. Nevertheless, WebQual primarily serves as a diagnostic
instrument and does not explicitly distinguish between attributes that merely prevent
dissatisfaction and those that can generate greater satisfaction [4,5,34].
While WebQual and Kano identify what users value and how specific attributes
influence satisfaction, neither framework directly translates these findings into operational
development priorities. This role is fulfilled by Quality Function Deployment [51]. Through
the House of Quality matrix, QFD systematically translates user requirements into technical
specifications, enabling organisations to prioritise improvement actions based on their
expected impact on user satisfaction and organisational objectives [15,51–53].
The integration of these three approaches establishes a sequential analytical process.
First, WebQual identifies the dimensions through which users evaluate website quality.
Second, the Kano Model classifies these attributes according to their influence on satisfac-
tion and dissatisfaction. Third, QFD transforms these insights into prioritised technical
requirements that guide redesign and development decisions. This progression enables
organisations to move from diagnostic evaluation to evidence-based intervention [15,52,53].
Previous studies have demonstrated the value of combining user-perception
models with requirement-prioritisation techniques across various digital contexts, in-
cluding e-government services, educational platforms, tourism websites and mobile
applications [49,54–56]. These studies consistently report improvements in the identifica-
tion of user requirements, prioritisation accuracy and alignment between design decisions
https://doi.org/10.3390/info17060606

<!-- Page 10 -->

Information 2026, 17, 606 10 of 33
and user expectations [ 15,52–56]. However, existing research remains fragmented, fre-
quently applying only partial combinations of these methodologies or focusing on isolated
dimensions of digital quality. Comprehensive frameworks that simultaneously evalu-
ate perceived website quality, classify user expectations and translate these findings into
technical priorities remain comparatively scarce.
The systematic review presented in Appendix A reinforces this observation. Although
previous studies have successfully applied combinations of WebQual, Kano and QFD
in domains such as tourism, digital health, e-government and higher education, few
studies have integrated all three approaches within a single evaluation framework that
links diagnosis, prioritisation and implementation. This gap is particularly evident in
institutional and territorial development platforms, where usability, information quality
and stakeholder engagement are critical success factors.
Furthermore, user-centred evaluations do not always converge with expert assess-
ments. Research on usability evaluation consistently shows that users and experts often
identify different categories of problems [39,41]. Users tend to focus on task accomplish-
ment, information clarity, and the experiential aspects of interaction, whereas experts are
more likely to identify issues related to interface consistency, accessibility, compliance, and
information architecture [39,41]. Consequently, combining user-based assessment with
expert heuristic evaluation can provide a more comprehensive understanding of website
quality than either approach alone.
Building on these considerations, the present study adopts an integrated WebQual–
Kano–QFD framework complemented by expert heuristic evaluation. In addition to the
three principal models, the heuristic checklist proposed by Veríssimo et al. [41] provides a
valuable complementary perspective by offering a comprehensive set of indicators covering
content quality, design, navigation and educational functionalities. This approach seeks
not only to assess the quality of the Interior+ platform from the user perspective but also to
identify the relative importance of quality attributes, prioritise improvement actions and
compare user perceptions with expert evaluations. By combining perceptual assessment,
expectation analysis, technical prioritisation and heuristic inspection, the proposed frame-
work contributes to a more comprehensive and actionable methodology for evaluating
institutional digital platforms.
Figure 1 summarises the conceptual framework guiding the study. WebQual di-
mensions are evaluated based on user responses, interpreted using the Kano Model, and
translated into technical priorities through QFD. These results are subsequently compared
with expert heuristic evaluations to examine areas of convergence and divergence in website
quality assessment.
Figure 1. Conceptual framework integrating WebQual dimensions, Kano-based expectation analysis,
QFD prioritisation and expert heuristic evaluation.
https://doi.org/10.3390/info17060606

<!-- Page 11 -->

Information 2026, 17, 606 11 of 33
In summary, the integration of the Kano, WebQual 4.0, and QFD models, comple-
mented by proposals such as Veríssimo et al. [41], constitutes one of the most comprehensive
and effective approaches currently available for evaluating digital usability. By combining
user-centred diagnosis, evaluative structure and strategic operationalisation, this articula-
tion not only identifies flaws or gaps but guides the design of more functional, intuitive
digital experiences aligned with the values and objectives of the institutions.
3. Materials and Methods
3.1. Research Design
This study adopted a mixed-methods design integrating user-centred evaluation, ex-
pert heuristic inspection and requirement-prioritisation techniques to assess the usability
and perceived quality of the Interior+ digital platform. The methodological framework com-
bined three complementary approaches, WebQual, the Kano Model and Quality Function
Deployment (QFD), supported by an independent expert evaluation based on established
usability heuristics.
The research design followed a convergent triangulation logic in which quantitative
user perceptions and qualitative expert assessments were analysed independently and
subsequently integrated through a QFD prioritisation process. This approach enabled
the identification of user expectations, the assessment of perceived website quality, the
detection of usability issues from an expert perspective and the translation of these findings
into prioritised design recommendations.
The methodological framework was informed by a preliminary documentary analysis
and a targeted literature review examining empirical applications of WebQual, Kano, and
QFD in digital service environments. Previous studies consistently demonstrated that inte-
grating user-perception models with prioritisation techniques improves the identification of
critical usability attributes and supports evidence-based design decisions [15,46,49,52–57].
To better explain the proposed methodology and for reproducibility, the operational
workflow of this study is summarised in Table 1.
Table 1. Operational workflow for multimodal usability evaluation.
STEP 1—Kano
→
STEP 2—WebQual
→
STEP 3—Heuristic
→
STEP 4—QFD
Input:
functional/dysfunctional
paired responses.
Output: SI/DI indices and
attribute categorisation.
Role: identify must-be,
attractive,
one-dimensional attributes.
Input: UX
Likert-scale scores.
Output: dimensional
usability measures.
Role: quantify
perceived quality.
Input: expert-based
UI/UX checklist
evaluation.
Output: flagged
technical and usability
issues.
Role: identify problem
areas not detectable
by users.
Input: results from
steps 1–3.
Output: weighted
WHAT× HOW
priorities.
Role: conversion into
actionable design
requirements.
In parallel with the user-based stages, an independent heuristic evaluation was
carried out by a group of UXD specialists. These experts applied a checklist based on
Veríssimo et al. [41], which covered criteria including content clarity, navigation, design
consistency, accessibility, and overall interface structure.
This expert evaluation served as a qualitative triangulation layer, providing an inde-
pendent baseline grounded in recognised usability principles and feeding the QFD matrix
as a secondary source of requirements, allowing for comparison between user perceptions
and expert diagnoses.
The use of expert evaluation in UXD and UID is widely supported. As argued
by Nielsen [42], heuristic inspection is efficient in early-stage diagnostics, enabling the
https://doi.org/10.3390/info17060606

<!-- Page 12 -->

Information 2026, 17, 606 12 of 33
detection of structural issues even without direct user participation. The model used here,
Veríssimo et al. [41], provides a validated and comprehensive framework for analysing
institutional websites.
This study follows a mixed-methods design with convergent predominance (see
Table 2), combining:
1. Quantifiable attitudinal instruments (Kano; WebQual 4.0) to measure expectations,
satisfaction levels, and perceived quality;
2. Qualitative heuristic analysis by experts to assess compliance with usability guidelines
and detect structural issues not visible in self-report measures;
3. QFD as an operational and decisional method to transform perceptions and heuristic
findings into prioritised design requirements.
Table 2. Methodological paradigm and complementarity of approaches.
Paradigm Method(s) Purpose Strengths Conceptual
Limitations
Contribution
to Triangulation
Attitudinal/Quantitative Kano Model
Measure user
expectations and
classify qualities
(must-be, attractive,
indifferent).
Calculate SI/DI.
Identifies critical
satisfaction drivers
and distinguishes
between basic and
attractive features.
Self-report bias: does
not capture real-time
behaviour;
dependent on
user awareness.
Provides
perception-based
priorities grounded
in
user expectations.
Attitudinal/Quantitative WebQual 4.0
Measure perceived
usability,
information quality,
and
interaction quality.
Standardised,
comparable metrics;
strong literature
foundation.
Purely perceptual;
sensitive to prior
familiarity; limited
behavioural insight.
Complements
Kano by
quantifying
satisfaction across
multiple
UX dimensions.
Qualitative/Heuristic Expert Checklist
Evaluation
Identify usability,
accessibility, and
interaction issues
using
design principles.
Independent of user
experience, it is fast
and identifies
structural issues that
surveys may miss.
Not based on actual
user behaviour;
subject to expert bias;
cannot detect
emotional responses.
Offers normative
evaluation baseline;
validates or
contrasts user
perceptions.
Operational/Decisional
QFD (Quality
Function
Deployment)
Prioritise design
requirements by
integrating user
and expert data.
Structured;
transparent; links
need to design
actions; produce
ranked
improvements.
Quality depends on
inputs; it does not
directly
measure usability.
Synthesises all
evidence into
actionable
design priorities.
These methods are epistemologically different and thus contribute complementary
forms of evidence. Their conceptual limitations justify the following triangulated design.
• Kano Model: Captures perceptions and expectations, but not real-time behaviour.
• WebQual 4.0: Provides perceptual metrics but may be influenced by familiarity or
subjective bias.
• Heuristic inspection: Identifies structural issues from a design-expert perspective but
does not reflect actual user behaviour or emotional reactions.
• QFD: Structures decision-making but depends entirely on the quality of inputs.
The integration of these layers overcomes the limitations of isolated approaches,
resulting in a more robust model for user-centred design, particularly in contexts involving
heterogeneous audiences and institutional digital services.
The adopted methodology aligns with recent empirical literature applying the Kano,
QFD, and WebQual models in digital environments. These studies similarly employ
structured surveys, attribute prioritisation, and multi-criteria analysis to capture user
expectations and translate them into design requirements.
https://doi.org/10.3390/info17060606

<!-- Page 13 -->

Information 2026, 17, 606 13 of 33
3.2. Website Context and Materials
The Interior+ platform (https://interiormais.pt/, accessed during April and May
of 2025) is an institutional website designed to boost and revitalise rural territories, pro-
viding information on support, funding programmes, entrepreneurship initiatives, inno-
vation cases, and contact details for local development entities. The website serves as
a central point of access to relevant resources and services for territorial actors, citizens,
entrepreneurs and regional organisations.
For this evaluation, the most frequent real tasks of users were considered, identi-
fied through preliminary navigation analysis and consultations with the website’s man-
agement team. Target tasks included: (1) locating information on available support or
funding; (2) consulting an innovation case; (3) downloading a resource/document; and
(4) contacting the responsible team/service. Before answering the Kano and WebQual
instruments, participants confirmed that they had performed at least one of these tasks on
the website, serving as a screening criterion to ensure a minimum level of familiarity with
the system.
Website analytics are routinely monitored by the project management team. However,
detailed traffic indicators were not consistently available during the study period and were
therefore not incorporated into the empirical analysis.
3.3. Study Context
The study focused on the Interior+ platform, an institutional website designed to
support rural development and territorial revitalisation initiatives. The platform provides
information on funding opportunities, entrepreneurship support, innovation projects,
training resources and regional development services.
To ensure meaningful evaluation, participants were required to have interacted with
the platform before completing the survey. Specifically, respondents confirmed that they
had performed at least one of the following common user tasks:
• locating information on support programmes or funding opportunities;
• consulting innovation case studies;
• downloading available resources or documents;
• contacting the responsible service or project team.
This screening criterion ensured a minimum level of familiarity with the platform and
reduced the risk of evaluations based solely on first impressions.
3.4. Participants
Two independent groups participated in the study.
User Sample: The user evaluation involved 40 participants recruited from the Interior+
platform’s target audience. Participants represented diverse demographic profiles and
levels of experience with institutional websites. The sample was predominantly female
(80%) and included individuals aged 18 to 64 years, residing primarily in inland regions
of Portugal.
Expert Sample: The heuristic evaluation was conducted by four specialists in User
Experience Design (UXD) and User Interface Design (UID). Two experts were senior pro-
fessionals with more than twenty years of experience in digital design and user experience
projects. The remaining two experts held doctoral qualifications in design and specialised
in usability and digital interaction research.
The use of a small panel of experienced evaluators is consistent with established
usability inspection practices, which indicate that a limited number of experts can identify
a substantial proportion of interface problems through heuristic evaluation [42].
https://doi.org/10.3390/info17060606

<!-- Page 14 -->

Information 2026, 17, 606 14 of 33
3.5. Data Collection Instruments
The user questionnaire was based on the WebQual framework developed by Barnes
and Vidgen [ 34], focusing on the dimensions of usability, information quality and
interaction quality.
To enable integration with the Kano methodology, the original WebQual attributes
were adapted into paired functional and dysfunctional questions. Functional questions
assessed users’ reactions to the presence of specific website attributes, whereas dysfunc-
tional questions explored reactions to their absence. This adaptation enabled the classifi-
cation of attributes into Kano categories while preserving the conceptual structure of the
WebQual dimensions.
The questionnaire included attributes related to navigation, responsiveness, informa-
tion clarity, visual design, privacy and security, and personalisation features.
The internal consistency of the adapted instrument was assessed using Cronbach’s
alpha. The resulting coefficient ( α = 0.836) indicated good reliability and supported the
instrument’s adequacy for analysing user perceptions.
The expert assessment employed the checklist proposed by Veríssimo et al. [41], which
comprises indicators organised into content, navigation, accessibility and visual design
dimensions. The checklist integrates established usability principles with contemporary
digital quality criteria, enabling systematic evaluation of institutional websites.
The expert evaluation provided an independent diagnostic perspective and served as
a complementary source of evidence for the subsequent prioritisation process.
3.6. Data Analysis
Responses to the functional and dysfunctional questions were analysed using the
Kano evaluation matrix. Attributes were classified as must-be, one-dimensional, attractive,
indifferent, or reverse, based on users’ response patterns [47].
To quantify the influence of each attribute on user experience, Satisfaction Index (SI)
and Dissatisfaction Index (DI) coefficients were calculated following established Kano
procedures [48,49]. These indicators estimate the potential contribution of an attribute to
user satisfaction when present and dissatisfaction when absent.
WebQual responses were analysed descriptively to characterise users’ perceptions
across the dimensions of usability, information quality and interaction quality. These
results complement the Kano classification by providing additional evidence regarding the
perceived quality of specific website attributes.
The findings obtained from the Kano and WebQual analyses were integrated into
a House of Quality matrix. User requirements (WHATs) were derived primarily from
attributes with higher potential for dissatisfaction (DI values) and lower perceived
quality scores.
Technical requirements (HOWs) were derived from the expert heuristic evaluation
and represented specific design interventions to address the identified user needs.
Relationships between WHATs and HOWs were coded using standard QFD rela-
tionship weights: 0 = no relationship; 1 = weak relationship; 3 = moderate relationship;
9 = strong relationship.
The priority score for each technical requirement was calculated as:
ˆPj = ∑
i
 
|DIi|·rij

where
ˆPj denotes the estimated priority score of requirement j in the QFD model;
https://doi.org/10.3390/info17060606

<!-- Page 15 -->

Information 2026, 17, 606 15 of 33
DIi represents the dissatisfaction index of attribute i, expressed in absolute terms
|DIi|;
rij is the relationship strength between attribute i and requirement j, typically coded as
0 (no relationship), 1 (weak), 3 (moderate), and 9 (strong);
∑
i
indicates the summation over all user attributes i associated with requirement j.
The resulting prioritisation enabled ranking of improvement actions by their expected
contribution to user satisfaction.
The results of the user evaluation and expert inspection were subsequently compared
to identify areas of convergence and divergence between user perceptions and expert
assessments. This comparison provided additional insight into how different stakeholder
groups perceive website quality and usability issues.
3.7. Ethical Considerations
Prior to data collection, an ethics application detailing the study objectives, recruitment
procedures, informed consent process and data protection measures was submitted to
the Institutional Ethics Committee. Due to administrative delays in the review process,
participant recruitment and data collection began while the application was still under
evaluation. Formal approval was subsequently granted under Protocol No. 9/2025 on
26 June 2025 without requiring substantive modifications to the study design or data
collection procedures.
Participation was voluntary, informed consent was obtained from all respondents, and
no personally identifiable information was collected. All data were analysed in aggregated
form and processed in accordance with the principles of the General Data Protection
Regulation (GDPR).
4. Results
In the case of the Interior+ project website, applying the Kano model revealed dis-
tinct patterns in how different attributes influence the user experience. Attributes such as
usability and responsiveness presented high Dissatisfaction Index (DI) values, indicating
that their absence generates strong dissatisfaction and therefore constitutes a priority for
intervention. Within the Kano framework, these attributes behave as must-be require-
ments, as users take their presence for granted and only notice them when performance
is inadequate.
Conversely, search personalisation and multimedia content were identified as attrac-
tive. Although not explicitly expected by users, their presence can significantly enhance
the user experience and represents a strategic opportunity for differentiation.
A particularly relevant finding concerns attributes associated with assisted usability,
such as persistent tutorials, extensive explanations, or intrusive help elements. These were
perceived negatively by users with higher levels of digital literacy, suggesting a reverse
effect in specific contexts. Rather than supporting interaction, such elements may hinder the
experience by reducing interface autonomy or fluidity. This result highlights the importance
of designing adaptive or optional support mechanisms rather than imposing guidance.
In parallel, the expert evaluation highlighted strengths in visual clarity, readability,
and graphic consistency, all of which contribute to the website’s institutional credibility.
However, experts also identified limitations in the depth of information and the con-
tent hierarchy, indicating that the platform does not yet fully accommodate diverse user
information needs.
The triangulation between user and expert perspectives revealed both convergence
and divergence. While both groups emphasised the importance of clarity, responsiveness,
and intuitive navigation, differences emerged regarding the usefulness of navigational
https://doi.org/10.3390/info17060606

<!-- Page 16 -->

Information 2026, 17, 606 16 of 33
aids. Elements such as explanatory menus and help features were valued by experts but
often rejected by more experienced users, underscoring the need for flexible, user-adaptive
design solutions.
Finally, the Kano results were integrated into the QFD matrix, enabling the translation
of user perceptions into prioritised technical requirements. Attributes such as usability and
security were identified as high priority due to their strong association with dissatisfaction.
This integration ensured that design decisions were grounded in empirical evidence, com-
bining user perceptions, expert evaluation, and structured prioritisation into a coherent
framework for intervention.
4.1. SI and DI Indexes
Table 3 presents the results of applying the Kano model, expressed as the SI and DI
for each attribute evaluated on the Interior+ website. These indices were calculated from
responses to the 40 surveyed users, allowing us to quantify the potential impact of each
attribute on the user experience.
Table 3. SI/DI indexes by evaluated attribute.
Attribute SI 95% CI (SI) DI 95% CI (DI) n(Users) “M + O”
(Dissatisfaction/Obligation)
Usability 0.463 [0.308; 0.618] −0.695 [ −0.838;−0.552] 25
Responsiveness 0.487 [0.332; 0.642] −0.681 [ −0.825;−0.537] 24
Visual Design 0.451 [0.297; 0.605] −0.553 [ −0.707;−0.399] 22
Quality of Information 0.420 [0.267; 0.573] −0.610 [ −0.761;−0.459] 25
Interaction/Contact 0.385 [0.234; 0.536] −0.512 [ −0.667;−0.357] 21
Security and Privacy 0.440 [0.286; 0.594] −0.580 [ −0.733;−0.427] 23
Customisation 0.360 [0.211; 0.509] −0.410 [ −0.562;−0.258] 18
The SI indicates the degree to which an attribute contributes to satisfaction; the closer
to 1, the greater the perceived positive effect. The DI, in turn, reflects the level of frustration
generated by the absence or malfunction of this same attribute; here, too, higher values
indicate a greater negative impact.
This approach allows us to distinguish among critical, attractive, and indifferent
attributes, providing an empirical basis for strategic design decisions. The analysis of these
data is fundamental for the subsequent construction of the QFD matrix, which translates
these effects into development priorities.
So, reading Table 3, is possible to observe that:
• Usability (SI = 0.463; DI =−0.695) and responsiveness (SI = 0.487; DI =−0.681) emerge
as the most critical attributes, exhibiting the highest dissatisfaction levels. Similarly,
the quality of information shows a substantial negative DI ( −0.610), indicating its
importance as a foundational component of the user experience.
• Attributes such as customisation (SI = 0.360; DI = −0.410) and interaction/contact
features (SI = 0.385; DI =−0.512) exhibit comparatively lower dissatisfaction effects,
suggesting they function more as value-adding elements than as essential ones.
• The column “n(users) M + O” shows the raw number of users whose Kano categorisa-
tion contributed to the dissatisfaction index (DI). This adds transparency to how DI is
derived and clarifies the behavioural weight of each attribute, showing, for example,
that 25 users contributed negative weight on Usability and Quality of Information.
The analysis of the SI and DI indices highlights usability and responsiveness as the
most critical attributes, with high dissatisfaction (DI) values indicating that their absence
or deficient execution strongly compromises the user experience. On the other hand,
https://doi.org/10.3390/info17060606

<!-- Page 17 -->

Information 2026, 17, 606 17 of 33
elements such as personalisation, multimedia integration, and visual aesthetics showed
positive satisfaction contribution (SI) indices while maintaining low dissatisfaction, which
characterises them as attractive attributes capable of positively surprising, though not
expected by all profiles.
These results reinforce the need to prioritise improvements to essential functional
components, while recognising the potential for differentiation through features with
emotional and symbolic value. The data collected from UID/UXD experts is then compared
with user results to identify convergences, discrepancies, and complementarities, and
subsequently integrated into the final QFD matrix.
4.2. Distribution by Categories Kano
The second stage of the analysis was based on the categorisation of attributes accord-
ing to the principles of the Kano model, which allows us to understand how different
functionalities affect the user experience in a nonlinear way. This approach classifies at-
tributes into four main categories, must-be, one-dimensional, attractive, and reverse, based
on their previously presented SI and DI scores.
The distribution of attributes across the Kano quadrants reveals the following consis-
tent and theoretically meaningful patterns.
• Attributes should not be classified as reverse attributes: High DI values instead point
to−0.695 and−0.681, meaning that their absence strongly impairs the experience,
thereby characterising them as must-be attributes within the Kano logic. The re-
sults clearly reveal that users take these elements for granted, whereas significant
dissatisfaction arises when they are poorly implemented. It could be that the only
components that would act like reverse attributes for those users with high digital
fluency are specific interface elements related to assistance, such as intrusive tutorials
or explanatory overlays that refuse to turn off, but not usability or responsiveness as
functional constructs.
• Attributes classified as must-be and one-dimensional: Clarity of information, up-to-
datedness, and security, are perceived as minimum requirements, the absence of which
causes high dissatisfaction, but whose presence is not a reason for enthusiasm.
• Attractive attributes: Personalisation and multimedia elements are not expected by all
users, but when present, they generate positive surprise and contribute to differentiation.
• Visual design attribute (SI = 0.451; DI = −0.553) falls within an intermediate zone,
suggesting a dual role. It contributes to perceived quality and differentiation but has a
less direct impact on dissatisfaction than core functional attributes.
To better visualise the relationship between the SI and DI indexes, Table 4 presents the
coordinate matrix used to position attributes according to their Satisfaction Index (SI) and
Dissatisfaction Index (DI).
This mapping highlights three distinct strategic zones. The first corresponds to a
critical intervention area, where attributes such as usability and responsiveness combine to
produce high dissatisfaction alongside comparatively low satisfaction, indicating that their
absence severely compromises the user experience. The second represents a baseline quality
zone, encompassing attributes such as information quality and security, which are perceived
as fundamental requirements whose absence generates dissatisfaction but whose presence
does not significantly enhance satisfaction. Finally, the attractive differentiation zone
includes attributes such as customisation and multimedia elements, which are characterised
by higher satisfaction and lower dissatisfaction, suggesting they serve as value-adding
features that enhance the experience without being strictly essential.
https://doi.org/10.3390/info17060606

<!-- Page 18 -->

Information 2026, 17, 606 18 of 33
Table 4. Kano Attribute Coordinates Matrix (SI/DI).
Attribute SI DI Kano Category Design
Priority Level Interpretation
Usability 0.463 −0.695 Must-be Critical Strong dissatisfaction when
absent; baseline requirement
Responsiveness 0.487 −0.681 Must-be Critical
Essential for access across
devices; failure is
highly penalised
Quality of Information 0.420 −0.610 Must-be/one-dimensional High Core content dimension;
affects trust and usability
Security & Privacy 0.440 −0.580 One-dimensional High Expected by users; directly
linked to perceived risk
Visual Design 0.451 −0.553 One-dimensional/attractive Medium
Enhances experience but is
less critical than
functional attributes
Interaction/Contact 0.385 −0.512 One-dimensional Medium
Supports engagement;
moderate
dissatisfaction impact
Customization 0.360 −0.410 Attractive Low Adds value but not expected;
opportunity for differentiation
The cross-reading between the quantitative data of the Kano model and the visual cat-
egorisation of Table 4 reinforces the need to concentrate improvement efforts on attributes
classified as critical, especially those with high perceived dissatisfaction. At the same time,
elements recognised as attractive, although not a priority, represent strategic opportunities
for differentiation, especially with users with greater digital literacy or aesthetic sensitivity.
Based on this analysis, the identified attributes were integrated into the QFD matrix,
which translates users’ voices into technical requirements and intervention priorities. This
final stage of the methodology constitutes the operative link between the evaluation of
the experience and the planning of future improvements, anchoring the design process in
systematised empirical evidence.
To operationalise user-expressed needs into concrete design actions, a reduced House
of Quality was constructed, as shown in Table 5. The Kano-derived DI values were used
as weighting coefficients reflecting the dissatisfaction potential of each attribute, while
WebQual responses provided semantic refinement. This allows for the translation of user
priorities into implementable design specifications.
In general, QFD prioritisation indicates that improvements to information retrieval
and navigational clarity (search, breadcrumbs, terminology) have the highest relevance
to users and the strongest potential to mitigate dissatisfaction. Personalisation and vi-
sual enhancement features, though, serve purely as secondary amplifiers rather than as
determinants of structural usability.
The fact that such attributes as Usability and Quality of Information present both
high DI magnitude and high M/O counts−25/40 and 25/40, respectively suggests that the
dissatisfaction potential is driven by an important share of the user base, not by extreme
outliers. This strengthens the claim that these attributes behave as must-be conditions
within the Kano logic structure.
To formally test H1a, one-sample t-tests (Table 6) were conducted on dysfunctional
response scores (scale 1–5), using the neutral midpoint (3) as the test value. In par-
allel, Wilcoxon signed-rank tests were applied to ensure non-parametric robustness of
the findings.
https://doi.org/10.3390/info17060606

<!-- Page 19 -->

Information 2026, 17, 606 19 of 33
Table 5. QFD calculation matrix: relationship weights (WHATs× HOWs) and priority scores.
HOWs
(Design Actions)
WHATs (User Attributes)—Weighted by |DI| Priority
Score
Usability
|DI| = 0.695
Responsiveness
|DI| = 0.681
Info Clarity
|DI| = 0.610
Security and
Privacy
|DI| = 0.580
Visual Design
|DI| = 0.553
Interaction
|DI| = 0.512
Customisation
|DI| = 0.410
Clarify terminology
and labelling 9 — 9 1 1 — — 12.88
Introduce
breadcrumb-based
navigation
9 — 3 — — 1 — 8.60
Implement
site-wide
internal search
3 — 9 1 — — 1 8.56
Improve
real-adaptive
mobile
responsiveness
— 9 1 — — 1 — 7.25
Increase visibility of
privacy and
cookies information
— — 1 9 — — — 5.83
Improve
communication and
support pathways
— — — — — 9 1 5.02
Implement
thematic filtering
and personalised
selection
— — 1 — — 1 9 4.81
Legend: Relationship strengths coded as: 9 = strong, 3 = moderate, 1 = weak, — = no relation. WHATs are
weighted by the absolute DI value of each attribute (Kano-derived). Priority score calculation: ˆPj = ∑
i
 
|DIi|·rij

.
Table 6. One-sample t-tests and Wilcoxon signed-rank tests for dysfunctional response scores.
Attribute Mean (M) SD t (df = 39) p (t-Test) Wilcoxon W p (Wilcoxon) Interpretation
Usability 4.65 1.08 9.70 <0.001 755.5 <0.001 Strong dissatisfaction
Responsiveness 4.60 1.15 8.80 <0.001 754.0 <0.001 Strong dissatisfaction
Information quality 4.40 1.45 6.12 <0.001 697.0 <0.001 Strong dissatisfaction
Visual design 3.85 1.75 3.08 0.004 — — Moderate dissatisfaction
Customisation 4.23 1.58 4.91 <0.001 — — Moderate dissatisfaction
Security and privacy 3.10 1.45 0.44 0.664 417.5 0.458 No significant deviation
The results indicate that usability, responsiveness, and information quality are all
significantly above the neutral midpoint. These findings indicate a strong dissatisfaction
effect associated with the absence of these attributes.
Visual design and customisation also differ significantly from the neutral point, albeit
with comparatively smaller effects. In contrast, security and privacy do not significantly
deviate from neutrality, suggesting a more ambivalent perception among respondents.
Overall, these results support H1a, confirming that the absence of essential system
attributes, particularly usability, responsiveness, and information quality, elicits statistically
significant dissatisfaction.
Although the Kano DI values for usability and responsiveness are high, indicating
potential dissatisfaction in the event of failure of these attributes, the questionnaire indi-
cates that no usability or responsiveness problems were reported by users (Table 7—0/40).
The high value of DI must, therefore, be due to the expectations-based potential for dis-
satisfaction rather than to any records of failure. This is the point where the distinction
between inferred dissatisfaction (Kano logic) and explicit dissatisfaction (user-reported)
comes into play.
https://doi.org/10.3390/info17060606

<!-- Page 20 -->

Information 2026, 17, 606 20 of 33
Table 7. Concordance between user-reported and expert-identified usability problems.
Attribute Users Indicating a
Problem (n/N)
Experts Indicating a
Problem (n/N)
Concordance (Problem
Seen by Both)
Usability (ease of understanding and use) 0/40 0/4 No
Responsiveness (device adaptation) 0/40 0/4 No
Clarity of information 17/40 0/4 No
Security of personal data 17/40 4/4 Yes
Clarity of privacy and cookies information 17/40 4/4 Yes
Personalisation of search/filters 0/40 0/4 No
Help texts (contextual help) n/a 4/4 No
Breadcrumbs/navigation trail n/a 4/4 No
Download options n/a 4/4 No
FAQ section n/a 4/4 No
As shown in Table 7, only two security-related attributes-both protection of personal
data and clarity of privacy/cookies information-converge: there, 17 out of 40 users and
all 4 experts flag this heuristic failure. In all other respects, users report issues (17/40)
where experts do not, with regard to information clarity, and several structural issues, such
as breadcrumbs, FAQs, download options, and contextual help, are detected by experts
alone and not assessed directly in the user questionnaire. Overall, concordance is limited,
supporting the view that user feedback and expert inspection provide diagnostic evidence
for different layers of usability.
This is because the latent nature of expectations explains the apparent discrepancy
between high DI values and the absence of user complaints: the DI represents latent expecta-
tions rather than consciously articulated problems. Therefore, usability and responsiveness
must be treated as must-be attributes, not reverse attributes.
The integration of Kano, WebQual, and QFD produced a prioritisation of requirements
that aligns with expert recommendations in key areas, particularly regarding information
clarity, navigation, and security. To assess H1b, the prioritised requirements generated
through the integrated Kano–WebQual–QFD framework were compared with the crit-
ical usability issues independently identified by the expert panel. Following previous
multimethod usability studies, convergence was operationalised as the proportion of high-
priority QFD recommendations that corresponded to issues also highlighted during the
heuristic evaluation.
The convergence index was calculated as:
Convergence(%) = Ncommon
NQFD
× 100
where
Ncommon represents the number of improvement priorities identified both by the
integrated Kano–WebQual–QFD framework and by the expert heuristic evaluation;
NQFD represents the total number of priority improvements identified through the
QFD analysis.
The QFD matrix identified five priority areas for intervention: usability, information
clarity, responsiveness, navigation structure, and visual consistency. Four of these priorities
were also independently identified by the UX experts during the heuristic evaluation.
https://doi.org/10.3390/info17060606

<!-- Page 21 -->

Information 2026, 17, 606 21 of 33
The resulting convergence rate of 80% exceeds the a priori threshold of 70% for H1b.
This result supports the hypothesis that the integrated Kano–WebQual–QFD approach
produces a prioritisation of design requirements that is substantially consistent with expert-
based usability assessment.
These findings confirm that the integrated methodological framework yields consistent
and robust prioritisation outcomes, effectively translating user perceptions into actionable
design requirements.
Differences between user and expert evaluations were examined using Fisher’s exact
tests. Statistically significant differences were observed for the security of personal data
(17/40 users vs. 4/4 experts; p = 0.044) and for privacy and cookie clarity (17/40 users
vs. 4/4 experts; p = 0.044), indicating meaningful differences in perception between the
two groups.
For clarity of information (17/40 users vs. 0/4 experts), the difference did not reach
statistical significance (p = 0.147). However, the magnitude of the discrepancy suggests a
potentially substantive effect that may not be adequately detected given the limited size of
the expert sample.
Overall, these findings provide partial support for H1c, evidencing statistically signifi-
cant differences in selected domains, particularly those related to security and privacy.
Table 7 summarises the concordance between user-reported issues and expert-
identified problems. Overall, the results indicate limited agreement between the
two perspectives.
In addition, Fisher’s exact tests confirm statistically significant differences only for
the security of personal data and for privacy/cookies clarity ( p = 0.044 for both), while
all other comparisons do not reach significance, likely due to the limited number of
expert evaluations.
These results provide partial support for H1c, suggesting systematic differences
between user and expert perspectives. Users predominantly report experiential and
perceptual issues encountered during interaction, whereas experts tend to identify
structural and latent usability deficiencies, including missing navigational aids and
support functionalities.
Therefore, it is possible to say that:
• RQ1, which examined how usability and information-quality attributes influence user
satisfaction and dissatisfaction, found that usability, responsiveness, and information
clarity exhibited the highest dissatisfaction potential (DI values), confirming their role
as critical quality attributes within the Interior+ platform. In contrast, personalisation
features and multimedia content were generally classified as attractive attributes that
contributed positively to the user experience when present but generated limited
dissatisfaction when absent. These findings support the proposition that different
website attributes exert differentiated effects on perceived value and user satisfaction.
• RQ2, which investigated whether the integration of the Kano Model, WebQual 4.0
and QFD could generate a consistent prioritisation of technical improvements, demon-
strated substantial convergence between user-derived priorities and expert recom-
mendations. The QFD matrix translated the attributes identified through Kano and
WebQual into actionable design requirements, while the comparison with the heuristic
evaluation revealed that four of the five highest-priority improvements were indepen-
dently identified by the expert panel. The convergence rate was calculated to be 80%,
exceeding the predefined threshold of 70%. This result indicates that the integrated
framework provides a coherent and operational mechanism for transforming user
perceptions into technical priorities.
https://doi.org/10.3390/info17060606

<!-- Page 22 -->

Information 2026, 17, 606 22 of 33
• RQ3 explored potential divergences between user perceptions and expert evaluations.
The results revealed both convergence and divergence patterns. While users and
experts agreed on the importance of usability, visual consistency and navigation
quality, a notable discrepancy emerged regarding information clarity. A considerable
proportion of users reported difficulties in understanding or locating information,
whereas this issue was not identified as critical during the expert heuristic inspection.
This finding suggests that user-centred and expert-based evaluation methods capture
different dimensions of website quality and therefore provide complementary rather
than interchangeable sources of evidence.
• H1a was supported by significant t-test and Wilcoxon results for usability, responsive-
ness and information quality.
• H1b was supported through the observed convergence between QFD-derived priori-
ties and expert recommendations, exceeding the predefined 70% threshold.
• H1c received partial support, as significant differences were observed for security-
related attributes, whereas information clarity differences did not reach statisti-
cal significance.
4.3. Heuristic Evaluation: Website Strengths and Weaknesses According to Experts
The qualitative evaluation was conducted by four experts in User Interface and User
Experience Design, based on the checklist developed by Veríssimo et al. [41], which com-
bines visual, functional, and structural criteria to assess the quality of institutional websites.
The technical analysis revealed solid performance of the website across the visual, struc-
tural, and typographic domains. Elements such as chromatic coherence, clarity of titles and
subtitles, organisation of information and graphic consistency were widely valued. These
aspects make a decisive contribution to smooth navigation, readability and the perception
of confidence in the interface, essential indicators of effective design.
The typographic clarity, the uniformity of the visual language, and the clear hierarchy
of the content stood out as high-quality dimensions, reflecting good practices in User
Interface Design. The adequacy of the layout to its communicative functions, as well as
the overall structure of the navigation, was also noted positively, revealing an effective
alignment between form and function.
Although specialists emphasise visual consistency, typographic hierarchy, and overall
aesthetic excellence, this does not conflict with the user-indicated potential dissatisfaction
with visual design. The distinction lies in the aspect under evaluation: experts view the
visual component as a fundamental element of interface quality, whereas users engage
with it primarily as a means of functional communication. Those with digital literacy
often benefit from clear visual cues and support, while highly literate users often see
excessive visual guidance as unnecessary. Thus, the apparent discrepancy does not reflect
contradictory evaluations, but rather different modes of perceptual engagement, aesthetic-
structural for experts and functional–operational for users.
On the other hand, the least valued aspects focused on specific functional absences,
such as the lack of an internal search tool, persistent help features, and content download
options. While not universal requirements, their omission may negatively affect certain user
profiles, especially those with lower digital literacy or more advanced expectations of con-
trol and exploitation. The absence of mechanisms such as breadcrumbs and contextual guid-
ance tools limits the interface’s scalability in more complex informational environments.
It is important, however, to highlight that the lack of a frequently asked questions
(FAQs) section, also mentioned by the experts, should not be automatically interpreted
as a failure. Given the predominantly descriptive and informative nature of the Interior+
https://doi.org/10.3390/info17060606

<!-- Page 23 -->

Information 2026, 17, 606 23 of 33
project and its lack of transactional functionality, this functionality may not be necessary
within the current framework.
In summary, the application of the checklist (Table 8) enabled the identification of
the website’s main strengths, including clarity, coherence, and aesthetics, while also high-
lighting concrete opportunities for functional improvement. These results complement
the data obtained from users and help consolidate an integrated reading of the platform’s
quality, supported by objective criteria for usability, accessibility, and alignment with the
institutional mission.
Table 8. Strengths and functional limitations identified by the experts [41].
Strengths (Positives) Limitations (Functional Absences)
Visual and typographic coherence Persistent lack of help features
Clarity and hierarchy of headings and subheadings Lack of breadcrumbs)
Organisation of information and good visual layout Lack of an internal research field
Graphic and colour consistency No content download options
Layout suitable for the communicative function No FAQ (with reservation, not necessarily negative)
The results confirm that usability attributes such as clarity and responsiveness are
essential for user satisfaction. These findings align with prior studies on institutional UX
design (e.g., [42,50]).
4.4. Triangulation and Integration of Findings
The expert evaluation, conducted by four UID/UXD specialists, identified clear
strengths in the website’s visual design, particularly in visual clarity, readability, and
graphic consistency. These aspects were considered to reinforce the platform’s institutional
credibility and overall professional appearance. At the same time, experts highlighted
important limitations, notably in the depth of information provided, the content’s structure,
and the extent to which the information architecture accommodates users with different
profiles and needs.
When compared with user findings, a pattern of both convergence and divergence
emerges. There is clear agreement between users and experts regarding the importance of
clarity, responsiveness, and intuitive navigation, which are consistently identified as core
determinants of quality. However, divergences arise regarding specific interface elements,
particularly navigational aids. While experts tend to value explanatory structures such as
enriched menus and guidance mechanisms as supportive of usability, experienced users
often perceive these same elements as potentially intrusive or unnecessary, suggesting
differences in expectations and interaction strategies between groups.
This triangulated interpretation is further reinforced by integrating the results into
the QFD (Quality Function Deployment) framework. Kano-derived dissatisfaction indices
were used as weighting factors in a reduced House of Quality, thereby translating user
perceptions into prioritised technical requirements. In this context, usability, responsiveness,
and information quality emerged as the highest-priority attributes due to their strong
association with dissatisfaction when underperforming. WebQual data complemented this
process by refining the semantic interpretation of user needs, supporting their translation
into actionable technical specifications.
The resulting QFD prioritisation indicates that improvements in information retrieval
mechanisms, navigation clarity (including search functionality, breadcrumbs, and termi-
nology consistency), and content structuring would have the greatest impact on reducing
user dissatisfaction. Conversely, features such as personalisation and visual enhancement,
https://doi.org/10.3390/info17060606

<!-- Page 24 -->

Information 2026, 17, 606 24 of 33
while still relevant to the user experience, function primarily as secondary contributors that
enhance perceived quality rather than address fundamental usability concerns.
The distribution of high dissatisfaction indices, together with substantial frequency
values for key attributes (e.g., usability and information quality), suggests that negative
perceptions are widespread across users rather than concentrated in isolated cases. This
reinforces their classification as must-be attributes, in line with Kano theory, and highlights
their foundational role in shaping user satisfaction.
Overall, the findings provide consistent empirical support for the proposed hypotheses
and the integrated methodological approach. Core functional attributes operate as must-
be requirements, generating strong latent dissatisfaction when absent or insufficiently
implemented. In contrast, enhancement attributes contribute to positive user experience
but do not constitute essential conditions for baseline satisfaction.
The triangulation between users and experts demonstrates that both perspectives
are complementary: users provide evidence of experienced and perceived interaction
issues, while experts identify structural and latent deficiencies that may not be immediately
visible to end users. Although alignment exists in key areas such as clarity and responsive-
ness, statistically and conceptually significant divergences remain, particularly regarding
navigation support features.
Finally, the combined application of Kano, WebQual, expert evaluation, and QFD
demonstrates strong methodological coherence and produces a robust, empirically
grounded prioritisation of design requirements. This integrated approach enables a more
comprehensive understanding of the user experience on institutional websites, supporting
evidence-based, user-centred redesign decisions.
5. Discussion
5.1. Website Quality and User Expectations
The findings demonstrate that the quality of institutional digital platforms cannot be
adequately understood through a purely technical or functional perspective. Consistent
with previous studies applying WebQual and Kano in digital environments [ 4,5,46,49],
users evaluated the Interior+ platform based not only on usability and interaction efficiency
but also on the clarity, accessibility and perceived usefulness of the information provided.
The Kano analysis revealed that attributes associated with information accessibility,
ease of navigation and content organisation exerted the strongest influence on dissatisfac-
tion when absent. This finding is consistent with the literature suggesting that informa-
tional attributes often function as must-be or one-dimensional requirements in institutional
websites [47–49]. Users tend to regard these characteristics as fundamental expectations
rather than value-added features, meaning that deficiencies can significantly undermine
perceived quality even when other aspects of the platform perform adequately.
The WebQual results further reinforce the importance of these dimensions. Although
participants generally reported positive perceptions of the website, lower evaluations of
information-related attributes suggest opportunities for improvement in content presen-
tation, organisation, and discoverability. Previous research has shown that information
quality is among the strongest predictors of satisfaction and trust in digital environments,
particularly in public and institutional platforms where users seek reliable and actionable
information [4,11,33].
These findings support the argument that website quality extends beyond technical
functionality and encompasses users’ ability to efficiently locate, interpret and apply infor-
mation to accomplish their goals. Consequently, the evaluation of institutional websites
should consider the usability, information quality, and interaction quality dimensions
simultaneously, rather than focusing exclusively on interface performance.
https://doi.org/10.3390/info17060606

<!-- Page 25 -->

Information 2026, 17, 606 25 of 33
5.2. Prioritisation of Improvement Actions Through the Integrated WebQual–Kano–QFD Framework
One of the main contributions of this study lies in the integration of WebQual,
the Kano Model and Quality Function Deployment within a single analytical frame-
work. While previous studies have applied these approaches independently or in partial
combinations [15,46,52–56], fewer studies have employed them sequentially to support
evidence-based prioritisation of website improvements.
The integration proved particularly valuable because it enabled the translation of
subjective user perceptions into operational design priorities. The Kano analysis identified
which attributes had the greatest potential to generate dissatisfaction, whereas WebQual
provided complementary evidence regarding perceived website quality. QFD subsequently
transformed these findings into a structured hierarchy of technical requirements.
The prioritisation process demonstrated that not all identified usability issues con-
tribute equally to the overall user experience. Some attributes exhibited relatively modest
quality scores but generated substantial dissatisfaction when absent, indicating that they
should receive priority attention during redesign processes. This finding reinforces the
value of combining satisfaction-based models with requirement-prioritisation tools rather
than relying exclusively on descriptive usability metrics.
Furthermore, the comparison between prioritised user requirements and expert rec-
ommendations revealed a substantial degree of convergence. The 80% convergence ob-
served between the QFD priorities and the expert recommendations provides empirical
support for the methodological integration proposed in this study. Although users and
experts approached the website from different evaluative perspectives, both groups identi-
fied largely similar priorities concerning usability, navigation efficiency and information
quality. This finding suggests that the integrated Kano–WebQual–QFD framework can
translate user perceptions into design priorities that are broadly consistent with established
usability principles.
The findings therefore support the proposition that combining WebQual, Kano and
QFD offers a practical mechanism for translating user expectations into strategic design
decisions, thereby strengthening the connection between usability evaluation and website
development processes.
The QFD analysis reinforced the patterns identified in the previous stages of the
study and demonstrated the practical value of integrating WebQual, the Kano Model and
Quality Function Deployment within a single analytical framework. Attributes associated
with usability, responsiveness, and information clarity, which exhibited higher potential
for dissatisfaction in the Kano analysis, emerged as the highest-priority areas for inter-
vention in the QFD matrix. This finding is consistent with previous studies applying
Kano–QFD integrations in digital environments, which similarly identified navigation
efficiency, information accessibility and service responsiveness as critical determinants of
user satisfaction [46,52–55].
The prioritisation process also highlighted the asymmetric nature of user expectations.
While attributes such as usability and information clarity were associated with basic or
performance requirements, personalisation features and multimedia resources emerged
as attractive attributes. These elements were positively valued by users when present but
did not generate substantial dissatisfaction when absent. Such findings support Kano’s
proposition that not all quality attributes contribute equally to user satisfaction and that
development efforts should be differentiated based on the role each attribute plays in
shaping the user experience [47–49].
The results further suggest that users of institutional platforms tend to favour solutions
that are integrated, intuitive and non-intrusive. Features that support navigation and
information access are appreciated when they operate seamlessly in the background rather
https://doi.org/10.3390/info17060606

<!-- Page 26 -->

Information 2026, 17, 606 26 of 33
than demanding continuous user attention. This observation aligns with the principle of
“invisible design” proposed by Maeda [ 54], which holds that the most effective digital
experiences minimise cognitive effort and enable users to accomplish their goals with
minimal friction. For a platform such as Interior+, which serves heterogeneous audiences
with diverse levels of digital literacy and domain knowledge, simplicity and clarity appear
to be more important than the proliferation of advanced features.
The prioritisation obtained through QFD therefore demonstrates how user-centred
evaluation can be translated into concrete development strategies. By identifying which
attributes generate the greatest dissatisfaction when absent and which features act as
differentiating elements, the integrated framework provides a structured basis for allocating
resources and guiding future redesign initiatives.
5.3. User–Expert Divergence in the Evaluation of Information Clarity
A particularly noteworthy finding emerged from the comparison between user per-
ceptions and expert evaluations. Although users frequently reported difficulties with
information clarity and content comprehension, expert evaluators did not identify these
concerns as major usability problems. This discrepancy illustrates how different evaluation
paradigms capture different dimensions of website quality.
At the same time, the triangulation process revealed important areas of convergence.
Both users and experts recognised the importance of visual clarity, consistency and coherent
information organisation. However, divergence emerged regarding specific orientation and
support mechanisms. Experts typically evaluate websites through established usability
principles, focusing on aspects such as navigation consistency, accessibility compliance,
visual hierarchy and information architecture [ 39,41,42]. Users, in contrast, assess web-
sites primarily through the lens of task accomplishment and practical information needs.
Therefore, some features considered useful from a design perspective were perceived
by users as unnecessary or excessive, suggesting that the value of interface elements de-
pends not only on their technical quality but also on how they fit users’ expectations and
behavioural patterns.
In the context of the Interior+ platform, experts may have considered the information
structure logically organised and compliant with accepted usability guidelines. From a
technical perspective, the content may have appeared appropriately categorised, accessible
and consistent with good design practice. However, users may have encountered difficulties
in interpreting the information, understanding specialised terminology or identifying the
most relevant content for their specific needs.
This distinction aligns with previous research suggesting that heuristic evaluation and
user testing frequently uncover different usability problems [39]. Whereas experts excel
at identifying structural and interface-related deficiencies, users are more likely to reveal
contextual and cognitive barriers that emerge during actual interaction with the system.
Information that appears clear to domain specialists may not necessarily be perceived as
clear by individuals with different levels of expertise, digital literacy or familiarity with the
subject matter.
The nature of the Interior+ platform may further explain this discrepancy. The web-
site serves a diverse audience that includes citizens, entrepreneurs, local development
actors and organisations. Such heterogeneous audiences often possess varying levels of
prior knowledge regarding funding programmes, territorial development initiatives and
institutional terminology. Consequently, information structures that appear self-evident to
experts may require additional contextualisation, simplification or guidance for end users.
From a practical perspective, this finding suggests that improving website quality
should not focus exclusively on structural usability characteristics. Equal attention should
https://doi.org/10.3390/info17060606

<!-- Page 27 -->

Information 2026, 17, 606 27 of 33
be devoted to content comprehensibility, plain-language communication and informa-
tion discoverability. Future redesign efforts could therefore benefit from adopting con-
tent design strategies, simplified terminology, clearer labelling systems, and user-centred
information architecture.
The identification of attributes classified as reverse within the Kano analysis further
supports this interpretation. Certain support and guidance mechanisms, traditionally
regarded as helpful usability features, were perceived negatively by some participants.
This finding may reflect increasing levels of digital literacy and user autonomy, particularly
among individuals accustomed to contemporary web navigation standards. Rather than
requiring extensive guidance, many users appear to prefer direct, self-explanatory interfaces
that minimise interruptions and unnecessary assistance.
These findings reinforce previous research indicating that expert evaluations and
user-centred assessments should be viewed as complementary rather than competing
approaches [39,41,42]. Whereas experts are particularly effective at identifying structural,
accessibility and consistency issues, users provide insight into contextual, cognitive and
experiential barriers that may not be apparent during heuristic inspection. The observed
divergence, therefore, strengthens the rationale for adopting multimethod evaluation
frameworks that integrate diverse perspectives on digital quality.
5.4. Implications for Institutional and Territorial Development Platforms
Beyond the specific context of the Interior+ platform, the study contributes to the
growing body of research advocating multimethod approaches to digital service evaluation.
The findings demonstrate that attitudinal instruments, heuristic inspections and prioritisa-
tion frameworks can be systematically combined to generate richer and more actionable
evidence than any single method alone.
The proposed framework advances current understanding of how perceptual, motiva-
tional and technical dimensions of usability interact within institutional digital environ-
ments. By integrating qualitative assessment through WebQual, expectation classification
through the Kano Model and technical prioritisation through QFD, the methodology
provides a structured mechanism for translating subjective perceptions into objective
design priorities.
From a practical perspective, this approach offers a replicable model for evaluating
public, educational and territorial development platforms. Such websites frequently serve
diverse user groups with varying needs, levels of expertise and digital competencies. Under
these conditions, design decisions must balance usability, accessibility, information quality
and resource constraints. The integrated framework assists decision-makers in identify-
ing which improvements are most likely to enhance user satisfaction while remaining
technically feasible.
More broadly, the results demonstrate that structured multi-model evaluations can
contribute to the development of more inclusive, equitable and user-centred digital services.
By systematically translating user perceptions and expert assessments into prioritised
technical requirements, organisations are better equipped to improve accessibility, clarity
and responsiveness, dimensions that are fundamental to the effectiveness of institutional
digital platforms.
The findings have broader implications for institutional websites and territorial de-
velopment platforms. Such platforms often perform multiple functions simultaneously,
including information dissemination, stakeholder engagement, service promotion and
resource access. As a result, they face particular challenges in balancing informational
complexity with usability and accessibility requirements.
https://doi.org/10.3390/info17060606

<!-- Page 28 -->

Information 2026, 17, 606 28 of 33
The results suggest that users prioritise clarity, ease of navigation and information
accessibility over more sophisticated or innovative interface features. This observation sup-
ports previous studies indicating that institutional websites are evaluated primarily on their
ability to facilitate efficient information retrieval and support goal-oriented tasks [4,11,33].
For managers and designers of territorial development platforms, the findings high-
light the importance of adopting evidence-based evaluation methodologies that incorporate
both user perspectives and expert judgement. The integrated framework proposed in this
study offers a possible approach to systematically identifying opportunities for improve-
ment and translating them into prioritised design interventions.
In addition, the study demonstrates the practical value of combining perceptual
evaluation, expectation analysis and technical prioritisation. Such integration may be
particularly useful for organisations operating under resource constraints, as it helps ensure
that redesign efforts focus on improvements most likely to enhance user satisfaction and
perceived service quality.
5.5. Limitations and Future Research
Several limitations should be considered when interpreting the results, and therefore,
they should be interpreted as exploratory rather than confirmatory.
First, the study relied primarily on self-reported user perceptions collected through
survey instruments. Although these methods provide valuable insights into satisfaction
and perceived quality, they do not directly capture actual user behaviour during interaction
with the website.
Second, the study relied primarily on perceptual survey data and heuristic inspection.
Behavioural usability indicators, such as task completion rate, time on task, navigation
paths, clickstream analysis, and error rates, were not collected. Consequently, the findings
reflect users’ perceived experiences rather than objectively observed interaction behaviour.
Future research should integrate behavioural and observational measures with perception-
based instruments to provide a more comprehensive assessment of website usability and
user experience.
Third, the expert evaluation involved a relatively small panel of four specialists. While
consistent with established usability evaluation practices, a larger and more diverse expert
panel could provide additional perspectives and strengthen the robustness of the findings.
Fourth, the study focused on a single institutional platform within a specific territorial
development context. Consequently, the generalisability of the findings to other types of
websites should be considered with caution.
Finally, no behavioural usability metrics were collected. Measures such as task com-
pletion rates, error rates, time-on-task, navigation paths or clickstream analysis could
provide complementary evidence regarding actual user performance and interaction pat-
terns. Future studies should consider integrating behavioural analytics with perceptual
and heuristic evaluation methods to obtain a more comprehensive understanding of digital
user experience.
Future research may also explore longitudinal applications of the integrated WebQual–
Kano–QFD framework, allowing researchers to evaluate whether prioritised improvements
effectively enhance user satisfaction over time and whether convergence between user
and expert evaluations changes following redesign interventions. Such studies could
combine perceptual, behavioural and expert-based evidence to generate a more holistic
understanding of digital service quality.
https://doi.org/10.3390/info17060606

<!-- Page 29 -->

Information 2026, 17, 606 29 of 33
6. Conclusions
This study proposed and validated an integrated framework combining WebQual,
the Kano model, QFD, and expert heuristic evaluation to assess and prioritise usability
improvements in the Interior+ institutional platform.
The results show that usability, responsiveness, and information clarity are the primary
determinants of dissatisfaction when underperforming, confirming their classification as
must-be attributes. Personalisation and multimedia content, in contrast, function as attrac-
tive attributes that enhance user experience but are not essential for baseline satisfaction.
The integration of Kano and WebQual outputs into QFD enabled the systematic
transformation of user perceptions into a prioritised hierarchy of technical requirements.
The most urgent improvements relate to navigation efficiency, information clarity, and
system responsiveness.
Triangulation between users and experts revealed both convergence (clarity, respon-
siveness) and divergence (navigation aids and support tools), confirming that these per-
spectives capture complementary aspects of usability evaluation.
Overall, the proposed framework demonstrates strong methodological coherence and
practical applicability, offering a replicable approach for converting user expectations and
expert assessments into evidence-based design decisions. It is particularly relevant for
institutional and territorial development platforms, where usability, clarity, and accessibility
are essential for effective digital service delivery.
Supplementary Materials: The following supporting information can be downloaded at https:
//www.mdpi.com/article/10.3390/info17060606/s1, Supplementary Data.
Author Contributions: Conceptualisation: D.R. and T.P . Methodology: D.R., F.V . and T.P . Investiga-
tion: D.R., F.V ., T.P ., JN. and T.F. Formal analysis: D.R., F.V ., J.N. and T.F. Writing—Original Draft:
D.R., F.V . and T.P . Supervision: D.R. Validation: D.R. and T.P . Visualisation: J.N. and T.F. Resources:
D.R. and T.P . Project administration: T.P . Funding acquisition: T.P . Writing—Review and Editing:
D.R., T.P ., J.N. and T.F. All authors have read and agreed to the published version of the manuscript.
Funding: This research was co-financed by Programa de financiamento—PRR—Plano de Recu-
peração e Resili ência, Medida—Agenda de investigaç ão e inovaç ão para a sustentabilidade da
agricultura, alimentação e agroindústria—componente Investimento e inovação, grant number PRR-
C05-i03-I-000233-LA7.2; LA7.5; LA7.6. The APC was supported by National Funds through the
Portuguese funding agency, FCT-Fundaç ão para a Ci ência e a Tecnologia, within the following
projects: BRIDGES—Biotechnology Research, Innovation and Design for Health Products, Polytech-
nic Institute of Guarda, https://doi.org/10.54499/UID/06407/2025, UID/PRR/06407/2025, and
UID/PRR2/06407/2025; NECE—Research Centre for Business Sciences, University of Beira Interior,
https://doi.org/10.54499/UID/04630/2025; CITUR—Centre for Tourism Research, Development
and Innovation, Polytechnic Institute of Guarda, https://doi.org/10.54499/UID/04470/2025.
Institutional Review Board Statement: The study was conducted in accordance with the Declaration
of Helsinki and approved by the Institutional Ethics Committee) of IPG ETHICS COMMITTEE—
GUARDA POLYTECHNIC UNIVERSITY (protocol No. 9/2025 at 26 June 2025).
Informed Consent Statement: Informed consent was obtained from all subjects involved inthe study.
Data Availability Statement: The data supporting the results reported in this study are available in
the Supplementary Materials accompanying this article. Supplementary contains the anonymised
raw responses from the user survey (n = 40) based on the Kano and WebQual 4.0 instruments. This
Supplementary File, also, contains the expert heuristic evaluation responses ( n = 4) collected via
the Veríssimo et al. checklist. And, finally the Supplementary File contains the full QFD calculation
matrix with relationship weights and priority scores. No additional datasets were generated or
analysed beyond those included in the Supplementary Materials.
https://doi.org/10.3390/info17060606

<!-- Page 30 -->

Information 2026, 17, 606 30 of 33
Conflicts of Interest: The authors declare no conflicts of interest. The funders had no role in the design
of the study; in the collection, analyses, or interpretation of data; in the writing of the manuscript; or
in the decision to publish the results.
Appendix A
Table A1. Applications of the Kano, WebQual 4.0 and QFD models in different digital contexts.
Study Models Used Research
Domain Platform Type Main Contributions Key Insight for This Study
He et al. (2023)
[55] Kano, QFD Smart tourism Leisure farming
mobile application
Demonstrated high accuracy
in translating user
expectations into functional
requirements for
application design.
Confirms the effectiveness of
integrating Kano with QFD
for transforming user needs
into prioritised
technical requirements.
Hidayat et al. (2017) [46] Web usability, Kano Higher education University website
Identified ten “true customer
needs” that significantly
improved website usability
and satisfaction.
Shows how Kano can
complement usability
evaluation models in
identifying critical
website attributes.
Cavacece et al.
(2024) [49] Kano Digital health Digital health
services platform
Identified critical,
performance, and attractive
attributes influencing user
experience in
healthcare services.
Reinforces the value of Kano
for identifying different types
of user expectations in digital
service environments.
Somasundaram et al.
(2020) [53]
Kano, QFD,
RAD, SWFMEA
Software
engineering
Software
development system
Proposed an integrated
framework for prioritising
user requirements in
software design.
Demonstrates how QFD can
operationalise Kano insights
in complex system
development processes.
Nindiaswari et al.
(2016) [55]
DeLone & McLean,
Kano, QFD
Information
systems
Electronic
processing system
Showed how integrated
models support
reprioritisation of user
requirements after
system adoption.
Highlights the importance of
combining perception-based
models with
prioritisation frameworks.
Sireli et al. (2007)
[57] Kano, QFD Information
systems
Product and service
information systems
Demonstrated how
Kano–QFD integration
improves product
development through
customer-driven design.
Provides foundational
evidence for linking customer
expectations with technical
design priorities.
Iranmanesh &
Tabrizi (2009)
[58]
QFD, Kano, ANP Web design Website evaluation
Identified critical website
design attributes through
multi-criteria
decision analysis.
Shows how decision-support
methods can enhance
prioritisation of
website improvements.
Heleno et al. (2016) [56] SERVQUAL,
Kano, QFD Digital banking Online banking system
Proposed an integrated
model for evaluating digital
service quality and
prioritising improvements.
Demonstrates the potential of
integrating quality
perception models with Kano
and QFD in service platforms.
Mansur et al. (2019) [52] SERVQUAL,
Kano, QFD E-government Digital public
services platform
Identified fourteen priority
attributes for improving
digital public service quality.
Indicates that integrated
models are particularly useful
in public digital
service contexts.
Sireli et al. (2007) [57] Kano, QFD Aerospace systems Aviation
information system
Developed a framework for
multi-product design based
on prioritised
customer requirements.
Shows the flexibility of
Kano–QFD integration across
complex
technological systems.
Li & Kim (2023) [59] Kano, QFD Cultural
heritage technology
Cultural heritage
mobile application
Demonstrated how
Kano–QFD integration
supports
user-experience-driven
design in
heritage applications.
Reinforces the applicability of
Kano–QFD integration in
digital platforms focused on
user engagement.
Chavez &
Namoco (2025)
[60]
Hesqual,
Kano, QFD
Higher
education services
University
administrative
service platform
Developed an integrated
framework translating
student needs into technical
service improvements.
Illustrates how service quality
models combined with Kano
and QFD can support
institutional digital
service optimisation.
https://doi.org/10.3390/info17060606

<!-- Page 31 -->

Information 2026, 17, 606 31 of 33
Table A2. Data collection and validation methods in studies with Kano, QFD and WebQual.
Study Data Collection Method Sample Size/Target Audience Applied Validation
He et al. (2023)
[55] Questionnaires, interviews Agricultural app users SUS scale,
quantitative validation
Hidayat et al. (2017) [46] Interviews, heuristic
usability measurement University Students Qualitative evaluation of the
degree of satisfaction
Cavacece et al. (2024) [49] Continuous,
unobtrusive analysis Users of digital health services Comparative evaluation
by attributes
Somasundaram et al.
(2020) [53]
Integrated
Framework (SURDCF) Software Users Requirements Modelling
and Prioritisation
Nindiaswari et al. (2016) [55] Case Study Users of the electronic
management system Attribute reprioritization
Mansur et al. (2019)
[52]
Integrated model with Kano
and SERVQUAL Citizens in public services Definition of critical
satisfaction attributes
Sireli et al. (2007)
[57] 12-step methodology Product
development stakeholders
Quantitative Integration
of Models
References
1. Ernungtyas, N.F.; Boer, R.F.; Qadrifa, S.S. The government website as user’s information source: A model of user satisfaction,
information, and system quality. Informasi 2024, 53, 197–214. [CrossRef]
2. Noor, M. The effect of e-service quality on user satisfaction and loyalty in accessing e-government information. Int. J. Data Netw.
Sci. 2022, 6, 945–952. [CrossRef]
3. Rasool, T.; Warraich, N.F. Does quality matter: A systematic review of information quality of E-government websites. InACM
International Conference Proceeding Series; Association for Computing Machinery: New York, NY, USA, 2018; pp. 433–442.
4. Nugraha, R.A.; Andriyanto, D.; Riana, D.; Khasanah, S.N. Analysis of Factors Affecting Quality of corona.jatengprov.go.id
Website Towards User Satisfaction using Webqual 4.0 Method.J. Phys. Conf. Ser. 2020, 1641, 012066. [CrossRef]
5. Putra, A.E.; Nataliani, Y. Analisis Kualitas Layanan Website Disdukcapil Kabupaten Semarang Diukur Menggunakan Instrumen
Webqual 4.0. J. Indones. Manaj. Inform. Dan Komun. 2023, 4, 895–903. [CrossRef]
6. Ardieansyah, A. Pengaruh kualitas website “Pejabat Pengelola Informasi dan Dokumentasi (PPID)” terhadap kepuasan pengguna
di Dinas Komunikasi dan Informatika Kabupaten Pemalang. J. Ilm. Adm. Pemerintah. Drh. 2022, 14, 101–110. [CrossRef]
7. Pourjahanshahi, F.; Mollahosseini, A.; Dehyadegari, S. Website quality and users’ intention to use digital libraries: Examining
users’ attitudes, online co-creation experiences, and eWOM. J. Retail. Consum. Serv. 2023, 74, 103393. [CrossRef]
8. Hertyana, H.; Lomotu, S.; Rahmawati, E. User Satisfaction Analysis of the PT Dikstra Cipta Solusi Website Using the Webqual 4.0
Method. J. Comput. Netw. Arch. High-Perform. Comput. 2024, 6, 1014–1024. [CrossRef]
9. Leite, P .; Gonçalves, J.; Teixeira, P .; Rocha, Á. A model for the evaluation of data quality in health unit websites. Health Inform. J.
2016, 22, 479–495. [CrossRef] [PubMed]
10. Husain, T.; Budiyantara, A. Analisis End-User Computing Satisfaction (EUCS) Dan WebQual 4.0 Terhadap Kepuasan Pengguna.
J. Tek. Inform. Dan Sist. Inf. 2018, 4, 164–176. [CrossRef]
11. Firdaus, M.B.; Puspitasari, N.; Budiman, E.; Widians, J.A.; Bayti, N. Analysis of the Effect of Quality Mulawarman University
Language Center websites on User Satisfaction Using the Webqual 4.0 Method. In 2019 2nd International Conference on Applied
Information Technology and Innovation (ICAITI); IEEE: New York, NY, USA, 2019; pp. 126–132.
12. Sibarani, R. Analisis Kualitas Website Universitas Satya Negara Indonesia Menggunakan Model Webqual 4.0. J. Satya Inform.
2024, 9, 21–31. [CrossRef]
13. Byun, D.H.; Finnie, G. Evaluating usability, user satisfaction and intention to revisit for successful e-government websites.
Electron. Gov. Int. J. 2011, 8, 1–19. [CrossRef]
14. Sachan, A.; Kumar, R.; Kumar, R. Examining the impact of e-government service process on user satisfaction.J. Glob. Oper. Strateg.
Sourc. 2018, 11, 321–336. [CrossRef]
15. Pourhasomi, M.H.; Arshadi Khamseh, A.; Ghorbanzad, Y. A hybrid of Kano and QFD for ranking customers’ preferences: A case
study of bank Melli Iran. Manag. Sci. Lett. 2013, 3, 845–860. [CrossRef]
16. Harsanto, B.; Prasetyo, S.C. Integration of Quality Function Deployment and Kano Model in Service Business. J. Manag. 2019,
23, 411. [CrossRef]
17. Kirgizov, U.A.; Kwak, C. Quantification and integration of Kano’s model into QFD for customer-focused product design.Qual.
Technol. Quant. Manag. 2022, 19, 95–112. [CrossRef]
https://doi.org/10.3390/info17060606

<!-- Page 32 -->

Information 2026, 17, 606 32 of 33
18. Gangurde, S.R.; Patil, S.S. Benchmark product features using the Kano-QFD approach: A case study. Benchmarking Int. J. 2018,
25, 450–470. [CrossRef]
19. Tan, K.C.; Shen, X.X. Integrating Kano’s model in the planning matrix of quality function deployment. Total Qual. Manag. 2000,
11, 1141–1151. [CrossRef]
20. Ginting, R.; Hidayati, J.; Siregar, I. Integrating Kano’s Model into Quality Function Deployment for Product Design: A Compre-
hensive Review. IOP Conf. Ser. Mater. Sci. Eng. 2018, 319, 012043. [CrossRef]
21. Ji, P .; Jin, J.; Wang, T.; Chen, Y. Quantification and integration of Kano’s model into QFD for optimising product design.Int. J.
Prod. Res. 2014, 52, 6335–6348. [CrossRef]
22. Afshan, N.; Sindhuja, P .N. Integration of Kano’s Model into Quality Function Deployment: A Review.IUP J. Oper. Manag. 2013,
12, 48–56.
23. Tontini, G. Integrating the Kano Model and QFD for Designing New Products. Total Qual. Manag. Bus. Excell. 2007, 18, 599–612.
[CrossRef]
24. Khoo, M.; Kusunoki, D.; MacDonald, C. Finding Problems: When Digital Library Users Act as Usability Evaluators. In 2012 45th
Hawaii International Conference on System Sciences; IEEE: New York, NY, USA, 2012; pp. 1615–1624.
25. Liu, Y.; Osvalder, A.-L.; Karlsso, M. Considering the Importance of User Profiles in Interface Design. InUser Interfaces; InTech.:
Rijeka, Croatia, 2010.
26. Christiansson, J.; Grönvall, E.; Saad-Sulonen, J. Mapping User Participation in the Design of Digital Public Services: Is Participatory
Design Relevant? In Participatory Design Conference 2024; ACM: New York, NY, USA, 2024; pp. 112–122.
27. Trischler, J.; Dietrich, T.; Rundle-Thiele, S. Co-design: From expert- to user-driven ideas in public service design.Public Manag.
Rev. 2019, 21, 1595–1619. [CrossRef]
28. Androutsopoulou, A.S.; Karacapilidis, N.I.; Loukis, E.N.; Charalabidis, Y.K. Combining Technocrats’ Expertise with Public
Opinion Through an Innovative e-Participation Platform. IEEE Trans. Emerg. Top. Comput. 2021, 9, 174–187. [CrossRef]
29. Boev, E.I.; Zotov, V .V .; Vasilenko, L.A. Digitalization of public administration: Expert reflection on problems and challenges.Digit.
Sociol. 2023, 6, 4–12. [CrossRef]
30. Gidlund, K.L. Makers and Shapers or Users and Choosers Participatory Practices in Digitalization of Public Sector. In Electronic
Government; Tambouris, E., Janssen, M., Scholl, H.J., Wimmer, M.A., Tarabanis, K., Eds.; IFIP International Federation for
Information Processing: Mödling, Austria, 2015; pp. 222–232.
31. Parasuraman, A.; Zeithaml, V .A.; Berry, L.L. Servqual: A Multiple-Item Scale For Measuring Consumer Perceptions of Service
Quality. J. Retail. 1988, 64, 12–40.
32. Chang, H.H.; Wang, Y.-H.; Yang, W.-Y. The impact of e-service quality, customer satisfaction and loyalty on e-marketing:
Moderating effect of perceived value. Total Qual. Manag. Bus. Excell. 2009, 20, 423–443. [CrossRef]
33. Napitupulu, D. Analysis of Factors Affecting The Website Quality (Case Study: XYZ University). Int. J. Adv. Sci. Eng. Inf. Technol.
2017, 7, 792. [CrossRef]
34. Barnes, S.J.; Vidgen, R.T. An Integrative Approach to the Assessment of E-Commerce Quality. J. Electron. Commer. Res. 2002,
3, 114–127.
35. Boothe, C.S.; Director, S.; Strawderman, L.; Burch, R.F.V .; Smith, B.K.; Bethel, C.L.; Holmes, K. Generalized User Experience
Questionnaire (UEQ-G): Holistic Measurement of Multimodal UX. J. User Exp. 2024, 19, 75–103.
36. Jääskeläinen, A.; Heikkinen, K. Divergence of User eXperience: Professionals vs. End Users. Age 2010, 25, 18–64.
37. Schrepp, M.; Kollmorgen, J.; Thomaschewski, J. A Comparison of SUS, UMUX-LITE, and UEQ-S. J. User Exp. 2023, 18, 86–104.
38. Koutsabasis, P . Beyond Specifications: Towards a Practical Methodology for Evaluating Web Accessibility. J. User Exp. 2010,
5, 147–163.
39. Alhadreti, O.; Mayhew, P . To Intervene or Not to Intervene: An Investigation of Three TA Protocols in Usability Testing.
J. Usability Stud. 2017, 12, 111–132.
40. Moon, E.; Schneider, S.M.; Ferronato, P .; Salah, M.; Ruecker, S.; McDonagh, D. The Role of Empathic Design Research in the
Prototyping of Interactive Visualizations. Des. J. 2019, 22, 1515–1527. [CrossRef]
41. Veríssimo, F.; Raposo, D.; Barradas, V .; Neves, J.; Silva, J.; Martins, N.; Brandão, D. A Checklist Proposal to Evaluate the Quality
of University Websites. In Advances in Design and Digital Communication II ; Martins, N., Brand ão, D., Eds.; Springer Nature:
Berlin/Heidelberg, Germany, 2022; pp. 134–145.
42. Nielsen, J. Usability Engineering, 1st ed.; Morgan Kaufmann: San Francisco, CA, USA, 1993.
43. Olsina, L.; Rossi, G. Measuring Web application quality with WebQEM. IEEE Multimed. 2002, 9, 20–29. [CrossRef]
44. Yoo, B.; Donthu, N. Developing a Scale to Measure the Perceived Quality of an Internet Shopping Site (PQISS). InProceedings of the
2000 Academy of Marketing Science (AMS) Annual Conference; Spotts, H.E., Meadow, H.L., Eds.; Springer Nature: Berlin/Heidelberg,
Germany, 2015; p. 471.
45. Loiacono, E.T.; Watson, R.T.; Goodhue, D.L. Webqual: A Measure of Website Quality 1. In Proceedings of the AMA Winter
Conference, Austin, TX, USA, 22–25 February 2002.
https://doi.org/10.3390/info17060606

<!-- Page 33 -->

Information 2026, 17, 606 33 of 33
46. Hidayat, S.; Wulandari, S.; Puspita, I. Analisis Kebutuhan Penggunaan Aplikasi I-gracias Menggunakan Integrasi Web Usability
Dan Model Kano (studi Kasus Mahasiswa Fakultas Teknik Universitas Telkom). In Proceedings of Engineering; Telkom University:
Bandung, Indonesia, 2017.
47. Kano, N.; Seraku, N.; Takahashi, F.; Tsuji, S. Attractive quality and must-be quality. J. Jpn. Soc. Qual. Control 1984, 14, 39–48.
48. Shahin, A.; Pourhamidi, M.; Antony, J.; Hyun Park, S. Typology of Kano models: A critical review of literature and proposition of
a revised model. Int. J. Qual. Reliab. Manag. 2013, 30, 341–358. [CrossRef]
49. Cavacece, Y.; Maggiore, G.; Resciniti, R.; Moretta Tartaglione, A. Evaluating digital health attributes for users’ satisfaction: An
application of the Kano model. TQM J. 2025, 37, 831–852. [CrossRef]
50. Zhang, P .; von Dran, G.M. User Expectations and Rankings of Quality Factors in Different Web Site Domains.Int. J. Electron.
Commer. 2001, 6, 9–33. [CrossRef]
51. Akao, Y. Quality Function Deployment: Integrating Customer Requirements into Product Design; Productivity Press: New York, NY,
USA, 2004.
52. Mansur, A.; Farah, A.N.; Cahyo, W.N. Integration of Servqual, Kano Model, and QFD to Design Improvement on Public Service
System. IOP Conf. Ser. Mater. Sci. Eng. 2019, 598, 012101. [CrossRef]
53. Somasundaram, J.; Sinha, N.K.; Dalal, R.C.; Lal, R.; Mohanty, M.; Naorem, A.K.; Hati, K.M.; Chaudhary, R.S.; Biswas, A.K.; Patra,
A.K.; et al. No-Till Farming and Conservation Agriculture in South Asia–Issues, Challenges, Prospects and Benefits. CRC Crit.
Rev. Plant Sci. 2020, 39, 236–279. [CrossRef]
54. Maeda, J. The Laws of Simplicity: Design, Technology, Business, Life; The MIT Press: Cambridge, MA, USA, 2006; ISBN 0262134721.
55. He, H.; Sun, W.; He, Y.; He, B. Research on Usability Design of Leisure Agriculture APP Interface Based on Kano-QFD. InDesign,
Operation and Evaluation of Mobile Communications; Gavriel, S., June, W., Eds.; Springer Nature: Berlin/Heidelberg, Germany, 2023;
pp. 29–39.
56. Nindiaswari, E.; Azzahro, F.; Hidayanto, A.N.; Gitik, S.; Anussornnitisarn, P . Integration of updated DeLone & McLean success
model, KANO model and QFD to analyze quality of an information system. In 2016 International Conference on Informatics and
Computing (ICIC); IEEE: New York, NY, USA, 2016; pp. 361–366.
57. Santos, A.H.M.; C ândido, C.J.F. Avaliação da qualidade dos serviços bancários online: Proposta de integraç ão dos modelos
SERVQUAL, Kano e QFD. Tour. Manag. Stud. 2016, 12, 145–153. [CrossRef]
58. Sireli, Y.; Kauffmann, P .; Ozan, E. Integration of Kano’s Model Into QFD for Multiple Product Design.IEEE Trans. Eng. Manag.
2007, 54, 380–390. [CrossRef]
59. Iranmanesh, H.; Tabrizi, B.H. An integrated framework for customer-oriented web design using QFD, Kano model and ANP . In
2009 International Conference on Computers & Industrial Engineering; IEEE: New York, NY, USA, 2009; pp. 1674–1679.
60. Chavez, J.C.; Namoco, C.J.S. Integrating HESQUAL, QFD and Kano framework for enhancing registrar services. Qual. Assur.
Educ. 2026, 34, 253–269. [CrossRef]
Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual
author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to
people or property resulting from any ideas, methods, instructions or products referred to in the content.
https://doi.org/10.3390/info17060606