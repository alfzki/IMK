# INTL_2024_User_Experience_Design_Professionals’_Perceptions_of_Generative_Artificial_Intel


<!-- Page 1 -->

User Experience Design Professionals’ Perceptions of 
Generative Artificial Intelligence 
Jie Li Hancheng Cao Laura Lin 
EPAM Stanford University Google 
Amsterdam, Netherlands Stanford, United States Mountain View, United States 
jie_li@epam.com hanchcao@stanford.edu lauralin.uxr@gmail.com 
Youyang Hou Ruihao Zhu Abdallah El Ali 
Notion Labs Cornell University Centrum Wiskunde & Informatica 
San Francisco, United States Ithaca, United States Amsterdam, Netherlands 
youyangh.biz@gmail.com ruihao.zhu@cornell.edu aea@cwi.nl 
ABSTRACT 
Among creative professionals, Generative Articial Intelligence 
(GenAI) has sparked excitement over its capabilities and fear over 
unanticipated consequences. How does GenAI impact User Expe-
rience Design (UXD) practice, and are fears warranted? We in-
terviewed 20 UX Designers, with diverse experience and across 
companies (startups to large enterprises). We probed them to char-
acterize their practices, and sample their attitudes, concerns, and 
expectations. We found that experienced designers are condent in 
their originality, creativity, and empathic skills, and nd GenAI’s 
role as assistive. They emphasized the unique human factors of 
“enjoyment” and “agency”, where humans remain the arbiters of 
“AI alignment”. However, skill degradation, job replacement, and 
creativity exhaustion can adversely impact junior designers. We
discuss implications for human-GenAI collaboration, specically 
copyright and ownership, human creativity and agency, and AI 
literacy and access. Through the lens of responsible and participa-
tory AI, we contribute a deeper understanding of GenAI fears and 
opportunities for UXD. 
CCS CONCEPTS 
• Human-centered computing → Empirical studies in HCI. 
KEYWORDS 
Generative AI, UX Designers, Responsible AI, User Experience, 
Human-AI Collaboration 
ACM Reference Format: 
Jie Li, Hancheng Cao, Laura Lin, Youyang Hou, Ruihao Zhu, and Abdallah El 
Ali. 2024. User Experience Design Professionals’ Perceptions of Generative 
Articial Intelligence. In Proceedings of the CHI Conference on Human Factors 
in Computing Systems (CHI ’24), May 11–16, 2024, Honolulu, HI, USA. ACM, 
New York, NY, USA, 18 pages. https://doi.org/10.1145/3613904.3642114 
Permission to make digital or hard copies of part or all of this work for personal or 
classroom use is granted without fee provided that copies are not made or distributed 
for prot or commercial advantage and that copies bear this notice and the full citation 
on the rst page. Copyrights for third-party components of this work must be honored. 
For all other uses, contact the owner/author(s). 
CHI ’24, May 11–16, 2024, Honolulu, HI, USA 
© 2024 Copyright held by the owner/author(s). 
ACM ISBN 979-8-4007-0330-0/24/05 
https://doi.org/10.1145/3613904.3642114 
1 INTRODUCTION 
The landscape of Articial Intelligence (AI) is rapidly evolving 
as adaptable foundation models, built on deep neural networks 
and self-supervised learning, have gained widespread adoption [ 6]. 
These span transformer-based large language models (e.g., GPT-3, 
BERT), visual (e.g., DALL-E, Florence), or multimodal (e.g., UniLM) 
models. The power of these models has recently been harnessed, 
exemplied by the launch of Generative AI (GenAI) tools, such as 
ChatGPT1 , DALL-E 22 , Stable Diusion3 , and Midjourney4 . These 
models have dramatically pushed forward the edge of AI capabili-
ties, where GenAI tools are capable of processing extensive data 
and learning statistical patterns, enabling them to generate novel 
multimodal output based on natural-language inputs (i.e., prompts). 
They have demonstrated the ability to produce diverse types of
content, including text [72], images [82], video [42], and audio [7]. 
For example, ChatGPT is viewed as the nest chatbot ever [ 36] 
with over a million people signed up to use it in only ve days [79]. 
Enthusiastic fans posted examples of ChatGPT producing computer 
code, essays, and poems; while others type in surreal prompts to 
Midjourney or DALL-E 2, ranging from requests like“paint a por-
trait of your boss patting a tiger in the style of Rembrandt”, to 
“depict a gathering of middle aged dinosaurs sipping coee and 
contemplating the meaning of life”, and these tools will return a 
startlingly accurate depiction in an instant. On the one hand, the 
widespread adoption of GenAI tools has sparked excitement within 
society due to their remarkable advancements; on the other hand, 
it results in anxiety about unanticipated consequences that may 
be implicitly induced and beyond human control [ 4]. Moreover, 
concerns arise regarding homogenization, as any weaknesses in 
these models have can propagate to downstream applications [6]. 
The expanding capabilities of GenAI have the potential to revo-
lutionize various aspects of modern life, and signicantly impacting 
individuals who earn their living by creating content, including 
designers, copywriters, journalists, and tenured professors. Among 
those professionals, there is a growing recognition of potential 
harms, such as reputation damage, economic and job loss, plagia-
rism, and copyright infringement [22, 25, 50, 75]. In the context of 
1ChatGPT: https://chat.openai.com
2DALL-E 2: https://openai.com/dall-e-2
3Stable Diusion: https://stablediusionweb.com
4Midjourney: https://www.midjourney.com

<!-- Page 2 -->

CHI ’24, May 11–16, 2024, Honolulu, HI, USA Li et al. 
participatory AI, it is of utmost importance to recognize that cre-
ative professionals and content creators, not just technical experts, 
possess valuable knowledge, expertise, and interests crucial for the 
responsible development of AI [5]. Several eorts are underway to 
explore the impact of AI on UX (e.g., AI in UX Research report [10]). 
As a step to better understand and address such growing concerns, 
in this paper, we specically explore the potential impact of GenAI 
tools on User Experience Design (UXD) practice, by involving UX 
Designers, important creative professionals, in our conversations. 
In contemporary UX Design, the goal is to align with both user 
needs and business values. Unlike other creative professions, UX 
Design is not purely artistic work, but revolves around meeting end 
users’ demands. This entails not only designing the overall look 
and feel of a digital product [96], but also involves crafting eective 
navigation systems, labels, and content categorization to ensure 
that users can eortlessly locate and access the information they 
require [40]. The UX Design process is an iterative, user-centered 
design process that requires designers to be creative and collabo-
rative, possess a problem-solving and sense-making mindset, and 
exhibit empathy towards users [ 73]. Successful UX Design must 
go through several iterations and is often linked to how well de-
signers manage to comprehend and translate users’ requirements 
into corresponding functionality and pleasing aesthetics [90]. With 
the ability to automate repetitive design tasks, such as creating 
wireframes, generating layout variations, or producing design pro-
totypes [45], GenAI tools can signicantly speed up the UX Design 
process, allowing UX Designers to explore a wider range of design 
options and iterate quickly to create more eective and engaging 
user experiences [81]. While GenAI tools oer many opportunities 
for UX Designers, it also presents potential threats related to job 
displacement, ethical concerns, lack of human touch, data quality 
and bias, and intellectual property issues [47]. 
2 RESEARCH QUESTIONS AND 
CONTRIBUTIONS 
To harness the power of GenAI in supporting UX Designers and to 
ensure the responsible disclosure of further AI advancements, our 
objective is threefold. First, we aim to gain an overview of current 
UX Design practices, including the tools used, their limitations, as 
well as the existing workows and challenges. Identifying existing 
practices and challenges provides a baseline against which the 
impact and utility of GenAI tools can be assessed. This also helps 
in contextualizing GenAI within current workows. For instance, 
larger enterprises and smaller companies often operate dierently 
in terms of UX design workows. Understanding these contexts is 
crucial for evaluating how GenAI tools might t into or potentially 
alter these various workows. Second, we seek to comprehend UX 
Designers’ perceptions toward GenAI – we intend to explore how 
UX Designers can leverage the potential of GenAI to overcome the 
existing limitations in tools and challenges in workows, allowing 
them to ultimately craft impactful and meaningful user experiences 
now and in the future. Lastly, we seek to understand how and in 
what capacity GenAI may impact User Experience Design (UXD) 
practice, and whether fears that may arise are warranted. To this 
end, we pose the following research questions (RQs): 
• RQ1: How do UX Designers perceive GenAI tools, and what 
is their view on the potential for incorporating these tools 
into their current workows? 
• RQ2: What opportunities and risks do UX Designers envi-
sion for the future of human-AI collaboration in UX Design 
practice? 
To address these questions, we conducted one-on-one in-depth 
interviews with 20 UX Designers who have diverse years of ex-
perience and currently work in companies ranging from startups 
to large enterprises with over 10,000 employees. These companies 
are mainly located in four countries across Europe and the United 
States. We interviewed participants to characterize their practices, 
and inquire about their attitudes, concerns, and expectations. 
Our work contributes to a deeper understanding of current UX 
Design practices, challenges as well GenAI fears and opportuni-
ties for UXD. We nd that overall, experienced UX designers are 
condent in their skills in terms of originality, creativity, and user 
empathy skills. They believe that GenAI can serve as an assistive 
tool to help with repetitive and general tasks, and for enhancing 
productivity – however, only for those who are already skilled 
designers. They emphasized the unique human factors of “enjoy-
ment” and “agency”, where humans will remain as the nal ar-
biters of “AI alignment” despite anticipations of future emergent 
AI abilities. However, they expressed serious concerns about skill 
degradation and unemployment, especially for junior designers, 
who may lose opportunities to systematically study design, and 
may instead end up being trained as prompters. Furthermore, they 
emphasized the importance of society paying sucient attention to 
potential problems that may arise with such GenAI advancements, 
such as copyright and ownership issues, adverse impacts on human 
creativity (“creativity exhaustion”) through GenAI output speed 
and homogenization, and concerns over promoting AI literacy and 
ensuring equal access to stay relevant. Ultimately, while UX Design 
practice may constantly be in ux, we believe GenAI’s impact on 
this profession requires immediate adaptation. We discuss the im-
plications of these ndings, within the lens of ensuring responsible 
AI development and human-AI collaboration within UX Design 
practice. 
3 BACKGROUND AND RELATED WORK 
3.1 AI’s Impact on (Creative) Work 
A key line of related literature studies the impact of AI on work. Fel-
ton et al. [27] suggest that the top occupations exposed to language 
modeling include telemarketers and a variety of post-secondary 
teachers such as English language and literature, foreign language 
and literature, and history teachers. Eloundou et al. suggests [23] 
around 80% of the U.S. workforce could have at least 10% of their 
work tasks aected by the introduction of large language mod-
els, while approximately 19% of workers may see at least 50% of 
their tasks impacted. Solaiman et al. [ 89] describe specic social 
impact GenAI systems may have over society – the framework 
denes seven categories of social impact: bias, stereotypes, and 
representational harms; cultural values and sensitive content; dis-
parate performance; privacy and data protection; nancial costs; 
environmental costs; and data and content moderation labor costs.

<!-- Page 3 -->

User Experience Design Professionals’ Perceptions of Generative AI CHI ’24, May 11–16, 2024, Honolulu, HI, USA 
Other works have empirically shown the considerable productivity 
gains through the use of state of AI tools such as ChatGPT [ 71, 77]. 
A number of works have discussed the impacts of AI on creative 
works, which are closely relevant to UX design and research [32]. 
Pearson [76] delves into the role of modern creative AI technolo-
gies as potential muses for artists and creators, highlighting their 
capacity to enable novel forms of image creation, music composi-
tion, animation, and video production. Kulkarni et al. [55] investi-
gates the use of text-to-image models (TTIs) in collaborative design 
through involving 14 non-professional designers. They reveal that 
TTIs facilitate rapid exploration of design spaces and support uid 
collaboration, with text prompts acting as reective design aids 
that facilitates exploration, iteration, and reection in pair design. 
Ning et al.[69] investigate the design space of Articial Intelligence 
technology-driven Creativity Support Tools (AI-CSTs), highlighting 
AI-CSTs’ impact on workows, their potential as co-creators, and 
strategies for handling AI errors, providing insights into AI-CSTs’ 
design and technology requirements. Epstein et al. [ 25] examine 
the impact of generative AI tools on traditional artistic practices, 
addressing questions of authorship, ownership, and the potential 
transformation of creative work and employment. Chang et al. [15] 
studied the perception of artists who leveraged text-to-image AI 
models for artwork, nding that 1) artists hold the text prompt and 
the resulting image can be considered collectively as a form of artis-
tic expression (prompts as art), and 2) prompt templates (prompts 
with “slots" for others to ll in with their own words) are devel-
oped to create generative art styles. Vinchon et al. [98] proposed 
four potential futures of AI human relationship for creative work, 
namely “Co-Cre-AI-tion", “Organic", “Plagiarism 3.0", and “Shut 
down". More closely related to the present work, Inie et al. [ 47] 
discussed creative professionals’ worries and expectations about 
generative AI, concluding that creative professionals should better 
understand, cope with, adapt to as well as exploit AI. Long and 
Magerko [63] provided a concrete denition of AI literacy by iden-
tifying 16 core competencies (e.g., recognizing AI, human role in AI, 
ethics) that humans need to eectively interact with and critically 
evaluate AI, along with 15 recommended design considerations 
that foster increased user understanding of AI (e.g., explainability, 
promote transparency, low barrier to entry). Complementary to 
the foregoing, we focus and conduct in-depth analysis dedicated to 
understand how AI impacts one specic occupation closely related 
to the HCI community – UX Design practice. 
3.2 Human-AI Collaboration for Human 
Empowerment 
The relationship between human and machine intelligence has 
been discussed since the early days of human computer interaction 
[44, 60]. Given the increasing performance and prevalence of AI in 
society, much attention have been drawn to study and design for 
eective and responsible human-AI collaboration in recent years. 
Amershi et al. [2] proposed design guidelines for human-AI inter-
action. Through multiple rounds of evaluation with practitioners, 
they condense over 150 AI-related design recommendations into 
18 aspects concerning four dierent time phases, and test their 
guideline against 20 AI-fused products with various categories 
(e.g., e-commerce, web search) and features (e.g., recommenda-
tions, search). Yang et al. [103] investigated whether, why, and how 
human-AI interaction exerts unique diculties in design. Through 
synthesizing prior research with their own design, research, and 
teaching experiences, they identied AI capability uncertainty and 
AI output complexity as two sources of unique design challenges of 
AI. Over two decades ago, Horvitz [44] presented a set of principles 
for building mixed-initiative user interfaces (UIs) that enable users 
and intelligent agents to collaborate eciently. The proposed prin-
ciples are still widely applicable to today’s human-AI collaboration, 
such as “providing mechanisms for ecient agent-user collabora-
tion to rene results” and “employing socially appropriate behaviors 
for agent-user interaction”. Lehman [ 58] also investigates mixed-
initiative human-AI interactions and collaborative work with gen-
erative systems. The author focuses on designing and evaluating 
functional prototypes through web-based experiments, exploring 
concepts like initiative, intent, and control, showing that the levels 
of initiative and control aorded by the UIs inuence perceived 
authorship when writing text. 
Kim et al. [ 52] used computational methods to categorize ten 
dierent AI roles prevalent in our everyday life and compared 
laypeople’s perceptions of them using online survey data, e.g., AI 
are considered with roles such as tools (low in both human in-
volvement and AI autonomy), servants (high human involvement 
and low AI autonomy), assistants (low human involvement and 
high AI autonomy), and mediators (high in both dimensions). They 
found that people assessed AI mediators the most favorably, and AI 
tools the least. Relatedly, Scott et al. [84] studied whether lay peo-
ple perceive AI as “conscious”, nding dynamic tensions between 
denial and speculation, thinking and feeling, interaction and experi-
ence, control and independence, and rigidity and spontaneity. Capel 
and Brereton [14] explored the emerging eld of Human-Centered 
Articial Intelligence (HCAI) by reviewing the existing literature 
on the subject. Their work identies established HCAI clusters, 
and highlights emerging areas, including Interaction with AI and 
Ethical AI. Additionally, they proposes a new denition of HCAI 
and encourage greater collaboration between AI and HCI research 
while suggesting new HCAI constructs. Similarly, Shneiderman 
[86] explored the concept of HCAI as a transformative approach 
to AI system design, emphasizing the importance of placing hu-
mans at the core of design thinking, oering three key ideas: (1) a 
two-dimensional HCAI framework that balances human control 
and automation, (2) a shift from emulating humans to empowering 
people, and (3) a three-level governance structure for creating trust-
worthy HCAI systems. These ideas propose a reframe in design 
discussions with the potential to yield greater benets for individu-
als, communities, and society, although they will require validation 
and renement through further research and development. Indeed, 
such HCAI methods [85] aim to ultimately produce Reliable, Safe & 
Trustworthy (RST) designs, fostering human self-ecacy, creativ-
ity, and responsibility while signicantly improving performance. 
Birhane et al. [ 5] reviewed participatory methods and practices 
within the AI and Machine Learning pipeline and acknowledged 
that wider publics beyond technical experts have knowledge, exper-
tise, and interests that are essential to the design, development, and 
deployment of AI. These prior works set the stage for ensuring, at 
both a research and policy level, for ensuring responsible human-AI

<!-- Page 4 -->

CHI ’24, May 11–16, 2024, Honolulu, HI, USA Li et al. 
collaboration that ultimately empower people and practices. We 
draw on these works to help interpret our ndings on how UX 
Designers envision current and future human-AI collaboration. 
3.3 Use of AI in UX Design and Research 
Studying User Interface (UI) and corresponding User Experience 
(UX), and how to build tools to better support UX design and 
research has long been a focal subject in the HCI community 
[12, 32, 53]. As AI increasingly shows its potential in transforming 
work practices, researchers have started studying and discussing 
the implications of AI for UX design and research [51, 90]. So far 
research has demonstrated the immense potential of AI for UX 
Design, with prototypes and applications available at key processes, 
including understanding the context of use, uncovering user re-
quirements, aiding problem solving, evaluating design, and for 
assisting development of solutions [1, 90]. Generally, most believe 
that AI will likely result in AI-augmented creativity support tools 
rather than a full transformative shift [61, 98]. Tholander et al. [92] 
investigated how generative machine learning and large language 
models may play a part in creative design processes of ideation, 
early prototyping and sketching, demonstrating practical useful-
ness and limitations of the system in design ideation processes, 
as well as how user interaction, and broader discourse around AI, 
shapes user expectation of AI’s capabilities and potentials. Feng et 
al. [28] found that UX practitioners can be more hands o when de-
signing prototypes since AI can provide support. They introduced 
in detail how UX practitioners communicate with AI and use AI 
as design materials for their daily work. Other works have also 
proposed specic prototypes to support better user experiences 
[38, 99]. Evaluations of such systems point to the potential of AI 
for augmenting human creativity, as AI often brings distinct per-
spective that opens up new avenues for artistic expression[16], and 
fosters a two-way exchange of ideas between users and AI [56]. Lin 
et al. [62] explored the design space of mixed-initiative co-creativity 
systems where humans and AI systems could communicate creative 
intent to each other. 
Meanwhile, research has also revealed challenges of incorpo-
rating AI into the UX design process. Gmeiner et al. [35] showed 
designers face many challenges in learning to eectively co-create 
with current generative AI systems, including challenges in un-
derstanding and adjusting AI outputs and in communicating their 
design goals. For example, when expecting AI tools to provide 
them with project-relevant work examples, or exhibit more context 
awareness for the specic problem at hand. Zhang et al. [106] fur-
ther demonstrated limitations of AI for architectural design, in that 
the AI tool “fails to understand the Architectural domain-specic 
terms" and “generates surreal images unsuitable for construction 
purposes". Other works demonstrate similar challenges of prompt 
engineering in using AI for product design [43]. On the other hand, 
Abbas et al. [1] found that while the majority of UX designers had 
no expertise with ML as a design tool, it holds great potential for 
improving productivity. Thoring et al. [93] dene a research agenda 
for GenAI-enabled design, highlighting key areas include creating 
better guided prompts, better interfaces for output interpolation, 
and getting AI to think outside of the latent space box (i.e., extrap-
olation). With regard to the potential of AI in UX research, Yang 
et al. [102] proposed a methodology to simulate user experience 
by using AI-aided design technology in mobile application design. 
Hamalainen et al. [ 37] leveraged OpenAI’s GPT-3 model to gen-
erate open-ended questionnaire responses about user experiences 
over video games, where they nd that GPT-3 can yield believable 
accounts of HCI experiences that is hard to be distinguished from 
real human responses. Park et al. [74] leveraged GPT-3 to simulate 
synthetic users and conversations over social computing platforms 
prototypes, where they nd generated responses are hard to be 
dierentiated from actual community behavior. By contrast to the 
majority of literature that focus on evaluating the use of AI for 
UX design and research in specic settings or technologies, our 
work contributes a deeper understanding of current practices, AI 
adoption, and perceptions of UX practitioners regarding emerging 
generative AI technologies, which sets the stage for envisioning 
how UX as a profession may evolve in the future with the ever 
increasing capabilities of AI. 
4 METHOD 
We employed a semi-structured interview methodology for this 
study [64]. We initially distributed a screening questionnaire with 
the goal of recruiting UX Designers who have diverse educational 
backgrounds and industry experiences, including years of experi-
ence, working at various company sizes, and residing in at least 
two dierent continents (namely Europe and North America). The 
screening questionnaire was distributed across social media net-
works (e.g., LinkedIn) and mailing lists (including design schools), 
targeting UXD communities. We received 48 responses, all of which 
were reviewed. While all respondents met our recruitment criteria, 
only 20 participants chose to participate. This mix of participants 
was well balanced in terms of our recruiting requirements. These 
20 participants engaged with us in online one-on-one 60-minute in-
terviews between April and July, 2023. 20 participants were deemed 
sucient given saturation points exceeding 17 interviews in socio-
logical research [41] and local sample size standards in HCI (remote 
interviews usually have M=15, SD=6) [ 13]. Each interview was 
conducted by an interviewer (author), while a second researcher 
(also author) was present to take notes. All interview sessions were 
additionally audio recorded. The interview process, data collection, 
and storage strictly adhered to the GDPR and ethical policy and 
data protection guidelines set forth by the last author’s research 
institute. 
4.1 Participants 
To ensure traceability in presenting the results, we labeled the 20 
participants as P1-P20. Among the 20 participants, there were 12 
females and 8 males. Three participants fell within the 18–25 age 
group, while 12 were in the 26–35 group. An additional ve partici-
pants belonged to the 36–45 age group. 11 of them had over ve 
years experience as UX Designers, two had three to ve years, and 
seven had fewer than three years of experience. For their experi-
ence using GenAI tools, all 20 participants used ChatGPT regularly, 
and eight of them regularly used GPT-4 (known as ChatGPT Plus). 
Thirteen participants tried Midjourney and occasionally used it for

<!-- Page 5 -->

User Experience Design Professionals’ Perceptions of Generative AI CHI ’24, May 11–16, 2024, Honolulu, HI, USA 
Characteristics UX Designers 
Work experience 
>5 years P1, P5, P6, P8, P10, P11, P12, P14, P16, P17, P18 
3-5 years P2, P7 
<3 years P3, P4, P9, P13, P15, P19, P20 
Company size 
>10,000 P5, P6, P7, P8, P9, P11, P14, P15, P16, P17 
1,000-10,000 P1, P2, P10, P13, P18 
500-1,000 P20 
<50 P3, P4, P12, P19 
Table 1: Years of work experience and company size (employee count) for our 20 UX Designer participants (P1-P20) 
Table 2: GenAI video demonstrations used in the interview 
GenAI video demos GenAI tools included Date posted on YouTube 
Crafting a mobile interface5 Midjourney (V4), Stability Photoshop Plugin (0.7.0) 
& ChatGPT (Jan. 30, 2023 version) 
Feb. 20, 2023 
Drafting a design proposal 
(only used the part of Notion 
AI: 4’18"-4’50")6 
Notion AI (2.21) Mar. 15, 2023 
Creating UI components 7 Prompt2Design (V3) May. 6, 2023 
Organizing ideation notes8 MiroAI (Beta) Mar. 8, 2023 
inspiration. Seven participants also mentioned their occasional use 
of Notion AI. Four tried Miro AI, and two used Bard. 
The 20 participants were from 15 dierent companies, with ten 
participants located in Europe, including The Netherlands, Sweden, 
Romania, Hungary, and the other 10 participants located across 
the United States. Moreover, ten participants were employed by 
enterprises with over 10,000 employees (across well known Big 
Tech9 companies), ve worked in internationally known enterprises 
with 1,000 to 10,000 employees, one was employed at a company 
with 500 to 1,000 employees, and four worked in small companies 
or startups with fewer than 50 employees. To ensure data privacy, 
we ensure that where participants work cannot be traced back to 
them (Table 1). 
4.2 Interview questions and procedure 
The interview questions are scripted to gather answers for the re-
search questions presented in Sec. 1, which are divided into four 
parts. Part 1 begins with general questions that aim to gather 
information about participants’ backgrounds, work experiences, 
common challenges in UX Design, and perceived limitations in 
their current tools. Part 2 comprises a set of questions focused on 
understanding participants’ current experiences and knowledge 
of GenAI tools, as well as their attitudes toward using GenAI in 
UX Design work. In Part 3, participants are shown a collection of 
videos consisting of four demonstrations from YouTube using vari-
ous GenAI tools for UX Design, ideation, research data synthesis, 
and front-end development work (Table 2). We used these video 
demonstrations primarily as probes to gauge our participants to re-
ect on these tools in general and how they relate to their practices, 
5Crafting a mobile interface: https://www.youtube.com/watch?v=_A_Jpr9HkGA
6Drafting a design proposal,: https://www.youtube.com/watch?v=R0gPrJsjsfU
7Creating UI components: https://www.youtube.com/watch?v=4Gt1NMf VlGQ
8Organizing ideation notes: https://www.youtube.com/watch?v=7u_EYv3ZXNw&t=3s
9https://en.wikipedia.org/wiki/Big_Tech 
and not to assess whether or not they have used these specic tools 
themselves. Subsequent follow-up questions delve into their im-
pressions of the GenAI tools shown in the videos, their envisioned 
roles for AI in human-AI collaboration, and their concerns regard-
ing ethics and ownership. Part 4 concludes the interview with 
questions soliciting further reections, advice or recommendations 
for UX Designers interested in integrating GenAI into their work 
and identifying their most desired, innovative functionalities of 
current and future GenAI. The complete list of interview questions 
is available in Supplementary Material A. 
The interview process lasted approximately 60 minutes and in-
volved the following steps: 
• Step 1 (5 mins): Introduction given by the interview fa-
cilitator to ensure participants understand the purpose of 
the interview, have read, comprehended, and signed the in-
formed consent form; 
• Step 2 (10 mins): General questions about background, 
workows, and UX practice; 
• Step 3 (20 mins): Attitudes, concerns, and expectations of 
GenAI Systems; 
• Step 4 (20 mins): Envisioning GenAI’s role in human-AI 
collaboration (including watching a video demonstration of 
a sample of current GenAI tools); 
• Step 5 (5 mins): Concluding questions. 
4.3 Data Analysis 
We used Miro10 for remote collaboration on data analysis. The au-
dio recordings of the interviews were transcribed. We analyzed the 
data following a deductive/inductive hybrid thematic analysis ap-
proach [29, 101]: First, the transcripts were coded by ve researchers 
using a deductive coding approach, where each researcher identied 
topics in the transcripts independently according to four categories 
10Miro: https://miro.com

<!-- Page 6 -->

CHI ’24, May 11–16, 2024, Honolulu, HI, USA Li et al. 
Figure 1: The analysis resulted in six major themes, where each theme contained two to four sub-themes. 
Figure 2: Eight categories of tools commonly used in UX Design practices 
in our code manual, created based on our research questions and 
interview guide. After the coding phase, the ve researchers held a 
half-day workshop to compare and discuss the identied topics and 
converted the coded data into 415 digital statement cards on Miro. 
Each statement card consists of the original quote from the par-
ticipant, participant ID (P1-P20), and a one-sentence statement or 
summary of the quote on the card. Instead of calculating statistical 
inter-rater reliability (IRR) for the analysis, the consensus among 
the ve researchers was reached through daily meetings, work-
shops and discussions [67]. Given that the categories in the code 
manual were still too broad, we then adopted an inductive coding ap-
proach [9, 17] to surface sub-themes from the statement cards using 
the anity diagramming technique [39], and to ensure the broader 
categories are consolidated. To help ensure our analysis meets the 
trustworthiness criteria (cf., [70]), we describe our hybrid approach 
in detail in Supplementary Material B. The analysis resulted in six

<!-- Page 7 -->

User Experience Design Professionals’ Perceptions of Generative AI CHI ’24, May 11–16, 2024, Honolulu, HI, USA 
•Summarize
design briefs and
technical
documentations
(P5, P6, P8, P18,
P19)
•Label the
information
according to
importance or
priority (P5, P9)
•Provide best
practices and
domain related
basic user
requirements
(P10, P18)
•Regenerate
based on human
created original
work (P1, P4)
•Provide
aesthetics and UI
inspirations (P1,
P2, P4, P6, P7,
P8, P9, P15, P19)
•Generate basic
wireframes and
“lorem ipsum”
texts (P1, P6, P9,
P10, P14, P12)
•Automate
responsive
design for various
screen sizes (P4,
P10, P12, P18)
•Check UX writing
(P5, P13, P18,
P19, P20)
•Run standard
usability or
accessibility
assessments (P1,
P2, P10, P17)
•Label and sort
qualitative data
based on
keywords (P10,
P12, P15, P16,
P17, P18)
•Suggest
directions for
design iterations
as a design
assistant (P13,
P14)
•Help make
presentation
slides (P13, P14)
•Reorganize
component
libraries and
design systems
(P5, P12, P13,
P14)
•Document design
assets and materials
for handover to
development teams
(P5, P13, P18)
•Communicate
with stakeholders
(P1, P5, P9, P15,
P16, P12)
•Adopt abstract
and systematic
reasoning (P15,
P19)
•Deeply
comprehend user
needs (P5, P9)
•Have empathy
toward users (P5,
P9, P15)
•Be original (P4,
P8, P10, P13,
P17)
•Communicate
and collaborate
as designer
peers do (P5, P9,
P16)
•Design user-
centered
functionalities
(P5, P7, P9, P15,
P18)
•Deprive
designers’
enjoyment of
design work (P8,
P16, P17)
•Replace real user
usability testing
insights (P14)
•Validate the data
analysis and user
testing results
(P1, P6, P8, P13,
P14, P15, P19,
P20)
•Communicate
and collaborate
as designer peers
do (P5, P9, P13,
P16)
•Address
feedback from
users with
empathy (P5, P9,
P15)
•Collaborate with
stakeholders to
examine whether
designs align
with business
goals and user
needs (P1, P12)
•Make final
decisions on
design solutions
(P1, P4, P8, P10,
P12, P13, P16,
P19, P20)
•Validate final design
implementations (P1,
P4, P8, P12, P13,
P16, P19, P20)
GenAI Can GenAI Cannot
Figure 3: Activities that can and cannot be completed by GenAI in the UX Design workow 
major themes (Fig. 1): (1) Limitations in current UX Design
tools: (a) frictional design hando; (b) fragmented tools; and (c)
lack of advanced design support. (2) Challenges in current UX
Design: (a) managing stakeholders expectations; (b) understanding
users; (c) satisfying both business and user needs; and (d) lacking 
domain knowledge. (3) UX Designers’ attitudes towards GenAI:
(a) overall impression of the videos; and (b) shortcomings of GenAI
tools in the videos. (4) Human-AI collaboration: (a) threats and
collaboration with GenAI; (b) work replaceable by GenAI; and (c)
work irreplaceable by GenAI. (5) Ethical concerns and owner-
ship: (a) originality, copyright, and ownership; (b) skill degradation,
and unemployment; (c) privacy, transparency, and equal access to
GenAI. (6) The future of GenAI in UX Design: (a) envisioning
collaboration with GenAI; (b) promoting AI literacy and accessibil-
ity for designers; (c) AI’s desired role in enhancing design processes;
and (d) challenges of dening AI-generated outcome metrics.
5 FINDINGS 
This section illustrates the current UX Design tools and workows, 
and provides a detailed presentation of the ndings under the six 
themes identied in the data analysis (Sec. 4.3 and Fig. 1). Fig. 3 
displays the activities in the UX Design workow that UX Designers 
in our study stated can and cannot be completed by GenAI. 
5.1 Current UX Design Tools and Workow 
Understanding the limitations and challenges of current UX design 
workows is crucial for creating a baseline to assess the impact 
and utility of GenAI tools. This knowledge not only informs how 
GenAI can address existing issues and enhance workows, but 
also aids in contextualizing these tools within dierent operational 
environments, from larger enterprises to smaller companies. This is 
essential for evaluating the integration and potential modications 
GenAI tools might bring to these diverse workows, where one 
size may not t all. Moreover, this understanding plays a key role 
in setting realistic expectations for the adoption of GenAI tools, 
providing insights into the aspects likely to be embraced or resisted 
by UX designers. 
We synthesized eight categories of frequently used tools that sup-
port UX Designers in their daily work (Fig. 2), as well as eight typical 
steps within UX Design practice – from gathering requirements 
from business stakeholders and users, to ideation, prototyping, user 
testing, iteration, and enabling the realization of solutions with the 
development team. Table 3 illustrates the main activities and tools 
used in each step. We observe that Figma was mentioned by all par-
ticipants as a design tool to support high-delity prototyping and 
hando to development teams. Miro was also frequently mentioned 
for brainstorming and synthesizing user research data.

<!-- Page 8 -->

CHI ’24, May 11–16, 2024, Honolulu, HI, USA Li et al. 
Steps Main Activities Tools 
1 Business Requirements • Analyze stakeholders’ requirements 
• Conduct a stakeholder kicko meeting to align on expectations, business objectives, 
and technical challenges. Brainstorm 
2 User Requirements • Dene research goals and identify the necessary features to achieve those goals. 
• Synthesize insights from user research to create personas and empathy maps. 
• Dive into user’s motivation, pain points, and challenges to inform design decisions. Brainstorm & 
User Research 
3 Ideation • Convert research insights into design ideas through sketches. 
• Conduct internal reviews to rene ideas with the design team. 
• Organize workshops with stakeholders to consolidate design solutions. 
Brainstorm, 
Documentation & 
Presentation 
4 Prototyping • Make interactive prototypes that visually and functionally represent the proposed 
design solutions. 
• Ensure prototypes capture user interactions, workows, and navigation paths. Design 
5 User testing • Conduct user testing to evaluate the prototypes. 
• Apply online (or oine) moderated (or unmoderated) user testing to guide partici-
pants through predened tasks. Communication
& User Research 
6 Iteration • Analyze user testing results, identifying areas for improvement. 
• Iterate on the design based on the gained insights Design & 
Non Digital 
7 Solution • Collaborate with stakeholders to ensure the design addresses user needs and aligns 
with the business goals. Documentation 
& Presentation 
8 Design Hando • Provide the development team with design assets and documentation and guide 
them to ensure the design’s consistency and accuracy across dierent screen sizes. 
• Address technical constraints and make UI adjustments to optimize the user 
interface for the nal product. 
Documentation, 
Presentation & 
Design 
Table 3: The typical UX Design workow in 2023 
In terms of workow, we observed that larger enterprises (with 
over 10,000 employees) often have clear divisions of roles between 
UX Designers, Product Managers, and UX Researchers. In contrast, 
smaller companies, such as startups with fewer than 50 employees, 
often lack such clear divisions. UX Designers in smaller companies 
are responsible for conducting user research and may spend more 
time convincing stakeholders to prioritize UX. Furthermore, work-
ows in smaller companies tend to be shorter than those in larger 
enterprises due to fewer people involved and lower communication 
costs. However, smaller companies may also omit or simplify some 
steps due to resource limitations, such as a limited budget for exten-
sive user evaluations. P6, who has experience working in both small 
companies and large enterprises, explained, “In large companies, 
our [UX Designers’] roles are well-dened. Although we also face a 
complex business landscape and stakeholders with dierent opinions, 
we have collaborators like UX Researchers and Product Managers 
to handle those aspects, and we can focus more on design. In small 
companies, we [UX Designers] must take on the roles of researchers, 
Product Managers, and designers. ”

<!-- Page 9 -->

User Experience Design Professionals’ Perceptions of Generative AI CHI ’24, May 11–16, 2024, Honolulu, HI, USA 
5.2 Theme 1: Limitations of Current UX Design 
Tools 
5.2.1 Limitation 1: Frictional design hando to development 
teams. Participants pointed out that handing over design specica-
tions, assets, and documentation to the development team is a rather 
frictional process. The current design tools do not support a seam-
less transition from design to development in a format accessible 
and understandable by the developers: “[We need] more gateways be-
tween designers and the developers, improving prototyping workows 
by enabling Figma prototypes to feed directly into the development 
coding workow, to reduce the frictions in communication between 
design and development teams.”[P14] 
5.2.2 Limitation 2: Fragmented Tools. Participants emphasized 
that the current UX Design tools are scattered. Each tool has spe-
cic strengths or functionalities, but transitioning seamlessly be-
tween them is challenging: “We use Miro for brainstorming and 
creating low-delity prototypes, and Figma for high-delity ones. 
However, transferring wireframes from Miro to Figma isn’t straight-
forward.”[P10] Some participants specically noted that the current 
design tools lack support for user research: “Something valuable 
would be the ability to conduct usability testing and generate data 
within the design tool itself.”[P17]. 
5.2.3 Limitation 3: Lack of Advanced Design Support. Par-
ticipants expressed dissatisfaction with the current design tools 
due to their lack of advanced support for complex animations, 
cross-platform designs, graphic design, and more intelligent design 
systems: “There are micro animation-type things that you don’t get 
from Figma, like the timelines that you would use in After Eects or 
Principle to ne-tune your animations.”[P17] “Design systems lack 
intelligence. I’d appreciate a design system that recommends suitable 
design components and automatically adjusts these components to t 
various screens.”[P5]. 
5.3 Theme 2: Challenges in Current UX Design 
5.3.1 Challenge 1: Managing stakeholder expectations and 
gaining buy-ins for UX.. The most frequently mentioned chal-
lenge is that UX Designers often spend over half of their time 
communicating and collaborating with a variety of stakeholders. 
This includes working with external vendors who take time to 
adapt to the work culture and style (P13), spending excessive time 
keeping stakeholders in sync, coordinating across time zones, and 
convincing them of the necessity of UX and gaining buy-in from 
management-level stakeholders (P1, P8, P12). Additionally, they 
must balance the expectations of stakeholders and clients with user 
needs to come up with an ideal solution (P18). P12 mentioned, “I 
have to convince others that UX is necessary and do a lot of work 
with developers to ensure the design is appropriately implemented. 
Some organizations take UX as lightly as a window dressing task and 
give more buy-in to the backend. So, we need to constantly educate 
them about the importance of scaling up UX. ”. Such management 
processes, stakeholder communication, and expectation alignment 
are aspects that heavily rely on crucial human-to-human commu-
nication, and an area which GenAI technologies do not currently 
support. 
5.3.2 Challenge 2: Understanding end-users. Participants men-
tioned that conducting research to understand user needs is chal-
lenging in terms of nding out the right pain points of users and 
building the right products: “I think the challenge always lies in 
trying to understand who I’m designing for, what their needs, goals, 
and problems are, and whether the product or service that I’m working 
on ts into the broader landscape.”[P17]. Such a challenge lies at 
the heart of UX Design and research [12]. While some approaches 
aim to simulate synthetic users and conversations (e.g., using GPT-
3 [74]), it is unlikely this can currently substitute for a deep under-
standing of end-users by designers. 
5.3.3 Challenge 3: Designing solutions that satisfy both busi-
ness value and user needs. Participants pointed out that coming 
up with good design solutions that balance clients’ needs, users’ 
needs, business value, and visual novelty is challenging: “The UX 
eld is quite mature, with existing design references and design sys-
tems aiding the work. The challenge is to come up with new ideas 
constantly and nd a balance when considering both established de-
sign references, internal stakeholders’ expectations, user needs, and 
incorporating them into the new design.”[P18] Satisfying business 
needs can carry implications for originality, copyright, and owner-
ship, all of which impact adoption (cf., Sec 5.6.1). 
5.3.4 Challenge 4: Lacking domain knowledge and resources. 
Participants mentioned that lacking domain expertise and resources 
to access knowledge poses a signicant challenge: “One of the chal-
lenges for UX Designers is acquiring extensive domain knowledge, 
such as creating designs customized for specialized elds like medi-
cal, automotive, ntech, and so on.”[P1]; “In a startup, we often face 
resource constraints that limit our access to experts, conducting user 
research or usability testing on a larger scale, which is crucial to en-
sure the feasibility and desirability of the products.”[P6]. We believe 
this may be a promising avenue by which GenAI tools, specically 
text-based large language models such as ChatGPT, can empower 
designers. Despite current model hallucinations (cf., [46]), design-
ers can have immediate, vast, and easy access to domain-specic 
information and resources. 
5.4 Theme 3: UX Designers’ Attitudes toward 
GenAI 
All participants agreed that GenAI tools can be powerful and con-
venient in supporting general tasks such as early-stage design 
ideation, basic UX writing, and basic coding. These tools provide 
a starting point for human designers to build upon, helping them 
overcome the fear of beginning from scratch. While many partic-
ipants were optimistic about the potential of GenAI tools, envi-
sioning these tools as a means to enhance design eciency, some 
others expressed mixed feelings towards GenAI. On one hand, they 
acknowledged that AI could assist with repetitive tasks, but they 
underscored that UX Design is inherently user-centered. The re-
liability of AI-generated designs is questionable, as they may not 
always align with user needs and goals. Relying too heavily on AI 
to design products or interfaces without human input was seen 
as risky. All participants emphasized that the current quality of 
AI outputs, such as text accuracy, image resolution, and design

<!-- Page 10 -->

CHI ’24, May 11–16, 2024, Honolulu, HI, USA Li et al. 
details and functionalities, still requires signicant human input 
and review, which may not necessarily save time. 
All participants believed that human designers possess unique 
abilities, as they exhibit empathy towards users and derive enjoy-
ment from the design process, even when starting ideation from 
scratch: “GenAI tools can help nowadays in generating basic ideas 
to help us populate the blank canvas, thereby aiding in overcoming 
the fear of the ‘empty canvas’. It’s similar to when we need to write 
reports; you can start with a basic structure generated by ChatGPT 
and then build upon it. However, I fear that in the long run, I might 
become more of an editor, gradually losing my design superpower to 
ll in the blank canvas and be empathetic towards users.”[P8]. 
5.4.1 Perceived shortcomings of GenAI tools shown in the 
demo. There were two shortcomings perceived to be key amongst 
participants: 
(1) Practicality and eciency. Participants highlighted that 
the GenAI tools showcased in the demos are quite generic, and the 
design process still requires a substantial amount of manual work. 
This includes tasks such as redrawing icons and buttons and in-
putting accurate text-based prompts. “Designers are trained to think 
visually. Our design process involves trial and error on sketchbooks. 
Designs emerge from numerous sketch trials, not from text-based 
prompts. [In the demo], you’re required to switch between various 
GenAI tools, Photoshop plugins, and perform a substantial amount of 
manual work, including redrawing and regenerating high-resolution 
images. I question whether these GenAI tools truly enhance the design 
workow.”[P12] 
(2) Accuracy and reliability. Participants questioned the over-
all accuracy and reliability of outcomes generated by AI tools. They 
hold the belief that human inputs are necessary to validate the AI-
generated outcomes. P16 shared: “For visual design, GenAI tools are 
still quite limited in capturing nuances and intricate details. Regarding 
ideation, AI tools like Miro AI may fall short in adequately represent-
ing the insights of stakeholders who possess extensive experience, say, 
20 years in a specializedeld like healthcare.”[P16]. P19 described
her negative experience using GenAI tools: “For Midjourney, I often 
found myself spending hours adjusting my prompts, yet still unable to 
achieve the envisioned results. As for Miro, the cards are only clustered 
based on keywords, requiring manual eort to create coherent clus-
ters.”[P19]. Furthermore, P3 expressed doubts about the reliability 
of AI’s code generation capability: “I’ve actually attempted to have 
ChatGPT generate code for certain features or functionalities, but it 
didn’t quite produce the results I was looking for.”[P3]. 
5.5 Theme 4: Human-AI Collaboration 
All participants described GenAI tools as helpers or assistants and 
recommended that “augmentation” and “enhancement” are good 
words to describe the assistance provided by GenAI in UX Design. 
5.5.1 Perceptions of threats and collaboration with GenAI. 
Participants expressed varying levels of concern regarding the po-
tential threats of GenAI. Some felt that if GenAI remained a generic 
tool under their control, it wouldn’t be a source of concern, while 
others worried about its ability to simulate designers’ reasoning. 
Recommendations included treating GenAI as a team member, with 
some participants emphasizing the importance of humans retaining 
ultimate decision-making power in human-AI collaboration. P18 
commented: “If the technology does eventually reach a point where it 
can accurately simulate designers’ rationales, then I might start wor-
rying about it.”[P18]. P19 recommended treating GenAI as a team 
member: “I would envision AI as part of the team, contributing to the 
overall process, but not solely responsible for the nal outcome.”[P19]. 
P8 stressed that humans should have the ultimate decision-making 
power in human-AI collaboration: “It should depend on people to 
choose which part I want AI assistance, for the purpose of expediting 
tasks. I don’t like the word ‘replace’. I very much enjoy the UI and UX 
Design...I want AI to be my apprentices. Humans do the creative and 
complex parts, and AI apprentices ll in the colors or draw lines.”[P8]. 
5.5.2 General and repetitive work can be replaced by GenAI. 
All participants shared the belief that GenAI has the potential to 
replace repetitive tasks, such as generating “lorem ipsum” texts for 
design mockups, condensing design briefs and technical documen-
tation, crafting repetitive design components, creating responsive 
designs for various screens, automatically documenting visual de-
sign elements into design systems, generating low-delity proto-
types, and generating design variations for inspiration (see Fig. 3: 
“GenAI Can”). As P8 said, “I envision AI functioning as a productivity 
tool that quickly aids me in concrete tasks. For instance, AI could sum-
marize PRDs [Product Requirement Documents] or explain technical 
backgrounds in plain language. Currently, these aspects require sub-
stantial eort from PMs [Product Managers] and engineers to convey 
to us designers.”[P8]. P12 expressed their wish for AI-supported 
responsive design, “I’m hopeful that GenAI can assist with tasks 
like responsive design for dierent screens and suggesting user ows 
across pages, not just on a single page.”[P12] Many other partici-
pants expressed their desire for GenAI support in various tasks, 
including providing design inspiration (P2, P4, and P8), as well as 
facilitating ecient UX writing (P18 and P19). P19 shared: “In our 
startup, we don’t have a dedicated UX writing role. Our designers 
often use ChatGPT to assess the appropriateness of the UX content in 
our design.”[P19]. 
5.5.3 UX Design work cannot be replaced by GenAI. Many 
participants made it clear that much UX Design work simply cannot 
be replaced by AI, including the work that requires communicat-
ing between human stakeholders, being empathetic towards user 
needs, and designing user-centered functionalities. They stressed 
the importance of humans being the original creator and validator 
of the AI outcomes (see Fig. 3: “GenAI Cannot”). 
(1) User inputs and human-human communication or col-
laboration. Participants condently expressed that they do not 
currently perceive GenAI as a competitor, since human designers 
serve as ambassadors for user needs and continue to be the ultimate 
decision-makers and arbiters of AI alignment. They emphasized 
that GenAI cannot replace work that requires user inputs, and 
human-human collaborations: “GenAI might be capable of taking 
over basic, repetitive, and straightforward tasks, but it cannot replace 
service design and collaborative eorts that demand more systematic 
and abstract thinking.”[P6]. P14 additionally pointed out, “UX De-
sign is not just about aesthetics, but also usability and the accessibility 
of elements. Real human users are essential for improving designs 
through actual user research and testing.”[P14]. P16 believed that 
human communication is not replaceable by AI, stating “I value

<!-- Page 11 -->

User Experience Design Professionals’ Perceptions of Generative AI CHI ’24, May 11–16, 2024, Honolulu, HI, USA 
insights from human colleagues, their experiences, ideas, and the 
knowledge they bring to the table. These do not have to be awless, 
but they aid us in charting directions together. I do not believe AI can 
perform this aspect of work.”[P16]. 
(2) Human creativity and decision making. Some partici-
pants pointed out that human creativity and originality are strong 
human qualities that are dicult to be replaced by AI. AI outcomes 
heavily rely on past data, potentially leading to recurring results 
due to the limited data pool. Human designers remain the driving 
force capable of deeply comprehending design contexts, empathiz-
ing with users, and innovating based on the latest knowledge: “The 
creative work that humans enjoy doing should not be replaced by AI. 
AI is a trained model that is based on the past, while human creativity 
and originality are more future-oriented.”[P8]; “Creativity can be sup-
ported by AI, as it can remix and regenerate based on human-inputted 
creative data, but humans possess the originality.”[P4]. 
Several participants stressed that nal decision-making cannot 
be delegated to GenAI. Human verication is deemed necessary 
for each stage of design and development projects: “AI must be 
intentionally used, monitored, and validated by humans. They are 
essentially Large Language Models, which are computers trained to 
converse like humans. The quality of the content and data provided 
by AI is not necessarily supported by actual research data veried by 
human researchers.”[P8]. 
5.6 Theme 5: Ethical Concerns and Ownership 
Copyright, privacy, data biases and transparency, skill degradation 
and unemployment, social disparity, and equal access are frequently 
mentioned ethical concerns among all participants. 
5.6.1 Originality, copyright, and ownership. Participants em-
phasized the signicance of crediting the original creators of art-
works or art styles utilized in UX work. P3 and P4 suggested that 
blockchain technology could be useful in ensuring direct owner-
ship attribution to the original creators, regardless of the extent to 
which the original work has been modied. P4 stated, “Ownership 
must remain traceable regardless of how extensively the AI outputs 
have been modied, derived, or reproduced from the originals. Perhaps 
blockchain can provide a solution here. ” P14 expressed her concerns 
over design plagiarism, “From the condentiality point of view, what 
data can be placed into GenAI tools, how we can make sure that we are 
using legal sources and we are not violating GDPR regulations. There 
are already cases that designers copy others’ work to build their own 
portfolios. GenAI can make plagiarism in design much worse.”[P14]. 
Expanding on the subject of ownership, some participants be-
lieved that humans must be the owners, with GenAI tools serving 
as supportive aids to humans in achieving the nal results. P11 
commented, “AI is not human; ownership belongs to humans. AI is a 
tool, much like Figma. I don’t believe ownership should be assigned to 
technology or tools. If you are the one rening, crafting the prompt, 
contributing creativity and thoughts to AI for generating the work, 
and overseeing the entire process, ownership should be attributed to 
humans.”[P11]. 
However, several other participants recommended attributing 
ownership to the part of work supported by AI or labeling it as 
AI-contributed and ensuring transparency about the tools used. P18 
provided a tting analogy, “The ownership attribution for using AI in 
future work should be similar to how researchers present their research 
ndings, mentioning the sources and systems used as references.”[P18] 
This was echoed by P19, “Ownership should be seen as a collective 
eort with input from various team members, including GenAI.”[P19]. 
5.6.2 Skill degradation and unemployment. Several partici-
pants highlighted their concern that human UX Design work might 
be less appreciated, potentially leading to complacency among 
human designers and a decline in their skills. They worry that 
AI taking over tasks previously considered essential for designers 
could contribute to skill degradation. These concerns, mentioned 
primarily by senior designers (refer to Table 1), are particularly 
relevant for junior designers, who could miss out on opportunities 
to further develop their skills. As such, human designers might 
transition into more managerial or generalist roles. P16 (a senior 
designer) envisioned this, stating, “Designers may fall into the trap of 
becoming complacent. Junior designers might have fewer chances to 
learn the design process but, instead, they may focus on mastering AI 
systems. Consequently, designers could evolve into generalists.”[P16] 
Participants specically highlighted that unemployment and 
skill degradation could evolve into signicant societal issues if not 
addressed seriously from the outset. P4 (junior designer) and P5 
(senior designer) expressed concerns that human designers’ skills 
might become narrow as we increasingly specialize in specic tasks 
if AI potentially takes over many parts of the work in the design 
workow, potentially limiting our creativity as designers: “AI can 
put us into a bubble. We feel that we are doing higher-level work, 
and the career barrier of becoming a designer is getting higher. But 
somehow we are forced to be more specialized in a limited range of 
tasks. The loss of oversight over the design and development workow 
may jeopardize our creativity.”[P5]. 
P12, also a senior designer, thoughtfully reected on the impact 
of GenAI on education and careers of junior designers, “Our exper-
tise matures through year-over-year practice, encompassing not only 
design skills but also design thinking and genuine user empathy. If 
companies decide to employ prompters or AI operators in the future 
to replace junior designers’ roles, how can these prompters or AI op-
erators receive the proper training equivalent to what we receive in 
design schools or through design practice? More importantly, how can 
junior designers acquire new skills or senior designers improve their 
expertise if AI takes over the tasks they need to practice and uphold 
their design skills?”[P12]. 
5.6.3 Privacy, transparency, and equal access to GenAI. Par-
ticipants pointed out that privacy is a signicant concern within the 
realm of GenAI. As these AI models ingest large amounts of data 
to learn patterns and generate content, there is potential for the 
unintentional exposure of sensitive information, such as personal 
or condential details that users did not intend to share: “If I want 
to use ChatGPT to extract information from technical documents, I 
don’t know how I should prevent sensitive information from being 
leaked. For my personal life as well, it is not clear how much of my 
personal data will be retained to further train the AI models.”[P19] 
Several participants stressed the importance of AI being trained 
on unbiased data and ensuring equal access to GenAI tools. This is 
due to concerns about social disparity and the potential for country 
policies to limit people’s ability to learn and access AI tools, as well 
as the possibility of biased data leading to questionable outputs.

<!-- Page 12 -->

CHI ’24, May 11–16, 2024, Honolulu, HI, USA Li et al. 
“Big companies and developed countries may gain control over the data 
fed into AI. It’s also easier for them to access GenAI tools compared to 
some developing countries.”[P6]. P2 added, “It is important to ensure 
that individuals who are relatively less educated and have limited 
knowledge of GenAI can still use these tools to enhance their work 
and daily lives.”[P2]. 
5.7 Theme 6: The Future of GenAI in UX Design 
Theme 6 provided insights into participants’ visions and desires 
related to the integration of GenAI in the eld of design. 
5.7.1 Envisioning collaborative design with GenAI. Some 
participants envisioned a triangulated system that involves collab-
oration and input from users, designers, and GenAI. This approach 
aims to minimize biases and ensure that crucial nuances, essential 
for design innovations, are not overlooked. As P11 mentioned, “Hu-
man designers may overlook certain nuances that could hold impor-
tance for users. I wish for GenAI to enhance this aspect by providing its 
input grounded in vast past data and knowledge, potentially elevating 
user experience design to the next level.”[P11]. 
5.7.2 Promoting AI literacy and access for designers. Several 
participants expressed a hope for increased AI literacy through 
education, beneting both experienced and junior designers. P13 
(a junior designer) noted, “Students may feel apprehensive about 
this signicant AI revolution. Education is essential to prepare both 
junior and senior designers for the impact of AI and how to leverage 
it to enhance our human design skills.”[P13]. Additionally, a few 
participants envision future AI tools to be more accessible for de-
signers. In other words, they desire AI tools that oer greater visual 
and intuitive usability, moving beyond sole reliance on text-based 
inputs. “The recent Apple Vision Pro headset is inspiring. Its visual 
and intuitive design appears promising. Thus, AI should also evolve 
to become more visual, intuitive, and universally accessible to all 
users.”[P12]. 
5.7.3 AI’s desired role in enhancing design processes. Many 
participants expressed their desire for GenAI to mature further, 
supporting them in various design tasks. They hoped that GenAI 
could assist in designing graphics, writing prompts, generating 
smart components, providing successful design examples, and au-
tomating the hando of designs to development teams. P4 noted, “I 
am anticipating easier ways to write prompts or automatically gen-
erate components that adapt to dierent screens, recommend smart 
animation transitions, and even generate 3D content for immersive en-
vironments in the future.”[P4]. Many other participants also voiced 
their desires for specic GenAI support in various tasks in the fu-
ture. For instance, they hoped AI could summarize state-of-the-art 
knowledge for research and strategy (P10, P18, and P19), serve as a 
synthetic user to expedite sprints (P1 and P18), oer professional 
guidance in accessibility design (P12), help designers quickly master 
and switch between dierent design tools (P18), aid in labeling and 
clustering qualitative raw data from user studies (P5, P9, P10, P12, 
and P18), and seamlessly translate designs into development (P5, 
P18, and P19). 
P18 specically highlighted the constantly changing landscape 
of design tools, expressing a desire for “GenAI to reduce the time 
designers spend keeping up with rapidly evolving technology. Design 
tools change every few years. If AI could help designers transition 
seamlessly between old and new tools or consolidate everything into 
a single tool, designers would have more time to understand user 
needs and design.”[P18]. P5 expressed a wish for “GenAI tools to help 
me assess the feasibility of designs on the development side during 
the early design stage and assist in documenting designs in Figma, 
facilitating smooth handos to the development team in a format 
accessible and understandable to developers. Currently, I still have to 
manually document designs, take numerous screenshots, and verbally 
explain them to the development team.”[P5]. 
5.7.4 The challenge of defining GenAI outcome metrics. Ac-
cording to several participants, another envisioned future for GenAI 
involves the challenge of dening metrics to measure the quality of 
AI-generated output. As P17 commented, “If many businesses use the 
same GenAI tools, it may result in similar designs and lacking diver-
sity and innovation. Also, AI can lead to generating numerous outputs 
and leave the challenge to us, humans, to choose among them.”[P17]. 
“It is already a challenge to select and ne-tune AI outcomes. We need 
guidelines on how to measure or validate AI’s output.”[P18] 
6 DISCUSSION 
Our key ndings indicate that experienced UX Designers acknowl-
edge GenAI’s potential as an assistive tool for repetitive tasks and 
productivity enhancement, yet they remain cautious about adopt-
ing GenAI tools themselves. This is due to their limitations in 
understanding user-centered design and their potential impact on 
their creative skills, as well as fundamental limits to enjoyment 
and agency in human-AI collaboration. While GenAI is seen as a 
game-changer in addressing challenges within current UXD prac-
tice, such as friction in design handos and limitations in UXD 
resources, designers expressed grave concerns about skill degra-
dation, particularly for junior designers. They advocate for GenAI 
tools to evolve into intuitive, visually-oriented, and collaboratively 
intelligent systems. This evolution aims to balance human creativity 
and AI eciency, emphasizing responsible AI use and human-AI 
collaboration to preserve human control in creativity and decision-
making. We delve into these aspects below, where we discuss im-
plications for human-GenAI collaboration, specically copyright 
and ownership, human creativity and agency, and AI literacy and 
access. 
6.1 Enjoyment and Agency in Human-GenAI 
Collaboration 
Enjoyment and meaning are two recurring key words in our con-
versations with UX Designers. As UX Designers not only aim to 
excel in their work but also seek to derive pleasure from it. Recent 
work has found that the user experience of early users of Chat-
GPT was impacted by hedonic attributes, not just pragmatic ones 
[88]. Enjoyment in work can be viewed through the lens of motiva-
tion theory, including both extrinsic and intrinsic motivations [48]. 
Extrinsic motivations revolve around whether the technology e-
ciently serves as a means to accomplish tasks, treating technology 
such as GenAI as a tool. Intrinsic motivations center on whether 
UX Designers nd their work inherently rewarding and the engage-
ment with technology enjoyable, considering technology such as 
GenAI as a toy [8]. We argue that, in UX Design, where creativity

<!-- Page 13 -->

User Experience Design Professionals’ Perceptions of Generative AI CHI ’24, May 11–16, 2024, Honolulu, HI, USA 
and problem-solving play central roles, this intrinsic motivation be-
comes paramount. Designers are not just driven by the end results; 
they also seek fulllment and enjoyment throughout the design pro-
cess. In other words, the future of AI-human collaboration should 
empower individuals to focus on tasks that truly matter to them, 
allowing AI to handle more mundane aspects. This approach not 
only enhances productivity but also fosters job satisfaction [59]. 
Closely related to enjoyment, we found that agency in human-
AI collaboration is also a recurring theme. Will AI take on more 
agency while humans play a supervisory role? Or will humans 
retain primary control and have the ability to override AI’s de-
cisions when necessary? Alternatively, will AI and humans col-
laborate in a mixed-agency approach, where both contribute to 
decision-making and execution [ 91]? UX designers believe that 
we should dierentiate between well-dened, routine tasks and 
complex, creative problem-solving tasks. Humans bring contextual 
understanding, ethical judgment, and accountability, and should 
lead complex work that requires creativity, empathy, ethics, and 
complex decision-making. Tasks led by AI and decisions made by 
AI should be transparent (cf., deceptive AI ecosystems [105]), ex-
plainable [21], and easily adjustable by human collaborators. The 
ideal scenario involves humans learning from AI insights, while 
AI improves based on human feedback (see e.g., [30] for a review 
on challenges for Reinforcement Learning from Human Feedback). 
Overall, we found that UX designers’ beliefs align with those of 
Fanni et al. [26], who advocate for “active human agency” and ar-
gue that AI policies should include provisions that enable users to 
promptly challenge or rectify AI-driven decisions (cf., contestable 
AI [66]). This approach aims to empower individual autonomy and 
bolster fundamental human rights in the digital age. We nd that 
the foregoing dimensions of enjoyment and agency to not only be 
unique human factors, but we suspect will increasingly play a role 
in the extent that UX Designers retain usage of such tools. 
6.2 GenAI Interpolating, Humans 
Extrapolating, and Creativity Exhaustion 
In today’s eciency-driven agile working culture, UX Design is 
essential for getting the design right and the right design [ 12]. It 
brings together a team to go through each sprint, progressing from 
idea to prototype to user research within short time frames [ 18]. 
GenAI’s remarkable speed in generating content and solutions 
have the potential to facilitate the fast-moving sprints. However, 
we must be aware that while GenAI can produce vast quantities 
of outputs in an instant, humans are the innovators behind these 
creations. Essentially, AI is interpolating, estimating values or gen-
erating outcomes within the range of existing data. Thoring et 
al. [93] approach this from the lens of evolutionary creativity the-
ory [87], where Variation and Selection are key components. While 
GenAI interpolates (Variation), it currently lacks the capability of 
extrapolating out of the latent space and continuing into unknown 
territory or merging into another latent space without supervisory 
human control (Selection) [93]. Indeed, AI might excel at “periph-
eral work” [ 83] or repetitive tasks within known data patterns. 
However, since AI is trained with known data, relying heavily on 
AI can lead to homogenized solutions (e.g., the AI-generated user 
interfaces all look similar) [6] or amplify biases in the data (e.g., the 
resulted design favoring certain demographic groups [4, 19, 25]. In 
contrast, consider children, who receive around four or ve orders 
of magnitude less language data than LLMs, and vastly outperform 
capabilities of AI [31]. Indeed, we humans excel at extrapolating, 
making predictions beyond the known data range using not only 
our creativity, intuition, and domain knowledge, but also benet 
from multimodal grounding and the social and interactive nature of 
received sensory input [31]. In essence, humans excel at the “core 
work” that they identify with, which contributes to not only their 
success, but also their happiness [83]. 
Another potential setback revolves around the danger of human 
creativity exhaustion in keeping up with the pace of GenAI output. 
GenAI’s relentless speed can exert immense pressure on human 
creators. While AI is not directly subject to physical factors like fa-
tigue [3], humans are expected to innovate continuously and rapidly 
on a large scale. On one hand, AI’s speed sets a challenging standard 
for human creators; on the other hand, it also lowers the training 
requirements to become an artist or a creative, as many people can 
create artistic paintings without picking up a brush. Moreover, as 
AI learns from human creations and renes its abilities, it raises the 
bar for what is considered innovative. Human creators in general, 
and UX Designer in particular, may feel compelled to push their 
limits to compete with AI, which can be mentally and emotion-
ally draining. To sustain human creativity, instead of competing 
with AI’s speed, human creators seem to be better o focusing on 
tasks that require critical thinking and emotional depth, where the 
human touch is irreplaceable. To that end, support systems and 
education should be introduced to alleviate the pressure on humans 
and help mitigate the risk of creativity exhaustion, a point to which 
we discuss next. 
6.3 AI Literacy and Participatory AI in UX 
Design 
In UX Design, there is a growing presence of tools with AI fea-
tures or supporting AI plugins. AI is gradually being integrated 
into various stages of the UX workow [ 65]. AI literacy begins 
with a fundamental understanding of AI concepts, including how 
machine learning works, the types of AI systems, their capabilities, 
limitations, and implications. This understanding is crucial for UX 
designers to harness AI’s power, ensure equal access to AI educa-
tion and tools, and actively participate in shaping and rening AI 
technologies, especially those used in their design processes. By 
adopting a participatory AI approach, UX Designers are part and 
parcel of the conversation around the future of GenAI development 
– this enables UX designers to strengthen their feedback and exper-
tise, ensuring that AI tools align eectively with human intentions 
and UX design practices [57, 63]. 
Another core element of AI literacy is that UX Designers should 
be able to think critically and question AI-generated outputs. There 
is a need for a comprehensive framework or guidelines for eval-
uating AI outcomes. Such a framework could encompass the as-
sessment of AI’s credibility, performance, accuracy, and impact 
on user experiences [ 89], as well as provide a structural means 
for contestability [66]. The foregoing echoes recent eorts [50] to 
ensure committees consisting of AI experts, ethics experts, and 
importantly creative professionals, are brought together to oversee

<!-- Page 14 -->

CHI ’24, May 11–16, 2024, Honolulu, HI, USA Li et al. 
GenAI’s progress. These groups would be best equipped to pro-
vide standards and best practices for evaluating GenAI output and 
mitigating harm on creative professionals (cf., [50]). 
6.4 Copyright and Ownership for GenAI Output 
in and beyond UX Design 
In our study, UX Designers emphasized the signicance of crediting 
the original creators of artworks or styles utilized in AI work. They 
mention the use of blockchain technology (cf., [24]), where of spe-
cial interest are computational provenance mechanisms [94] that 
track and document the origins, processes, and transformations of 
AI-generated content or artifacts. As such, this involves recording 
information about how a piece of content, such as text, images, 
or other media, was generated, which AI models and algorithms 
were used, and any data sources that contributed to the creation 
of the content. In so doing, this would facilitate the attribution of 
ownership should they draw on model output throughout their UX 
practice. We found that many UX Designers in our study believed 
that humans should be the owners of the design outcomes. However, 
this was so only if GenAI tools serve as supportive aids, and human 
designers remain in the driver seat by leading the entire process, 
adding detailed touches and synthesizing user inputs. However, 
they recommended attributing ownership to the part of the work 
supported by AI or labeling it as AI-contributed while ensuring 
transparency about the tools used. Interestingly, in a recent study, 
Draxler et al. [ 20] found that people often do not disclose AI as 
an author when using personalized AI-generated texts in writing, 
although they attribute ownership to the AI. Comparing human and 
AI ghostwriters, they found that attributing authorship to oneself is 
more prevalent when writing with AI support. Given disagreement 
in attributing ownership, it is necessary to develop an authorship 
attribution framework that takes the user and their relationship to 
the generative model into account. 
The discourse around copyright, privacy, ownership for UX de-
sign practice is inherently connected to the wider discourse on 
GenAI as a whole. Whether dealing with text, images, or video, the 
foregoing raise the question of whether the GenAI output being 
generated is ethical and legally compliant to begin with. Indeed, 
recent work by Jiang et al. [ 50] in assessing the impact of visual 
GenAI on artists paints a bleak picture regarding the outspoken 
harms on artists, which can well extend to other creative works (in-
cluding the work of UX designers). For example, “fair use” within 
US copyright law may not always end up protecting the artist, 
whether due to case-by-case determination, or the high cost in 
pursing legal battles. Whether the way forward constitutes better 
watermarking approaches to ensure copyright and traceable ac-
countability [94, 107], or the further development of regulation and 
policy at an (inter-)national level (e.g., European AI Act11 [97]), it 
is clear GenAI development needs to be acted upon responsibly -
for and beyond UX Design practice. As such, we believe drawing 
on the key human-centered principles (e.g., aligned with human 
well-being, respecting privacy, and having appropriate governance 
and oversight) of responsible AI development [34] are of immediate 
necessity to protect designers moving forward. 
11https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52021PC0206 
6.5 The Future of GenAI-infused UX Design: 
Fears and Opportunities 
The rapid advancements in GenAI and UX Design underscore the 
necessity of ongoing monitoring and research in both elds. As 
GenAI tools continue to evolve, it is essential to ensure that they 
align with human values, ethics, and creative processes, despite 
any uncertainty that may arise from currently unresolved empirical 
and conceptual issues in human psychology [11]. To that end, by 
answering our research questions of current (RQ1) and future 
(RQ2) perceptions of GenAI, this study serves as a foundation for 
exploring the opportunities and challenges presented by GenAI in 
UX Design, where we emphasize the importance of responsible and 
informed collaboration between humans and AI in this domain, 
which leads to the question: are such fears of GenAI for UX Design 
warranted? 
We observed (Sec. 5.5) that experienced UX Designers’ were de-
fensive about the very idea that “AI can potentially replace human 
designers”. Experienced designers, on the one hand, have con-
dence in their superpowers in terms of design skills, the collision of 
wisdom and enlightenment in human-human communication, and 
possessing high empathy towards users. However, they emphasized 
(Sec. 5.6) the real risks that GenAI could pose on the junior UX 
Design workforce, posing the dilemma: if junior human design-
ers don’t do the mundane work that can essentially be replaced 
by GenAI, then how will they reach the seniority levels wherein 
GenAI cannot replace? On the other hand, even experienced de-
signers raised fears about AI in general, and GenAI in particular, 
and how this may in the future render their expertise partially ob-
solete. Specically, some concerns revolved around emergent AI 
capabilities, where as AI becomes more sophisticated (e.g., more 
parameters with more diverse and larger training data), there is 
the possibility of it advancing beyond the intended scope or con-
trol [6, 80]. On the ip side, some of our participants may not have 
been aware of the rapid pace of developments – for example, GenAI 
models can be ne-tuned on unique stakeholder datasets [ 104], 
which would elevate ideation, brainstorming, and documentation 
within the UX design process. Nevertheless, the risks persist should 
even ne-tuned models lead to situations where GenAI systems 
generate designs or make decisions that are not aligned with re-
ned user experience principles, stakeholder satisfaction, or worse, 
violate human values, ethics, or cultural norms [ 100, 108], even 
when designers may take the driver seat of selecting and rening 
the output with additional prompts (cf., [ 15]) on custom-trained 
models. These concerns align with user perceptions of machine 
consciousness (of GPT-3) [84], which lead to several tensions, of 
which most relevant to our use case are interaction and experience, 
control and independence, and rigidity and spontaneity. Further-
more, as in digital art, people who exhibit strong anthropocentric 
creativity beliefs may be biased to brush o GenAI design output 
as overall less creative and awe-inspiring should they know it was 
made with GenAI [68]. 
However, unpredictability, polarity, and such tensions often sig-
nify new opportunities as emerging AI capabilities can lead to 
innovative problem-solving approaches and entirely new design
concepts that while inspire human creators, can radically disrupt

<!-- Page 15 -->

User Experience Design Professionals’ Perceptions of Generative AI CHI ’24, May 11–16, 2024, Honolulu, HI, USA 
the practice (reminiscent of paradigmatic shifts in the natural sci-
ences [54]). However, while we already see a radical disruption to 
several elements of UX Design practice (cf., Fig. 3), much remains 
to be desired (and cautious about) as GenAI capabilities increase. 
Essentially, we contend that ensuring harmonious alignment be-
tween human-AI collaboration for UX Design practice, methods and 
strategies are required to ensure that GenAI systems comprehend 
and respect human designers’ values and interpret and respond to 
their concerns eectively. For this, we call upon further research in 
and beyond responsible AI to continue placing the human at the 
center of technology development, and importantly, on reconcilia-
tion eorts should ethical values dier amongst groups [49]. Indeed, 
as Rakova et al. [78] argue, to better enable responsible AI work, or-
ganizations need to update their prevalent practices, which requires 
addressing prevalent work practices, emerging work practices, and 
mapping their aspirational future. To this end, a path forward is to 
continue drawing on participatory AI and value-sensitive design 
[5, 21, 33, 47] to create AI for social good [95], and ultimately foster 
human and creative safeguarding mechanisms, allowing UX Design 
practice and its practitioners to adapt and ourish gracefully. 
6.6 Study Limitations and Future Work 
In our investigation, we opted for a breadth-rst approach to better 
understand the overall impact that GenAI may have on UX De-
sign, which naturally comes at the cost of depth – we did not delve 
deeper into any particular UX products, tools, or workows. As 
such, prioritizing breadth over depth was strategic, enabling the 
capture of a wide range of perspectives and considerations within 
the UX eld. This serves as an important stepping stone for fu-
ture works to delve into specic tools and use cases to provide a 
more in-depth analysis. Second, our interviews were limited by 
the small sample size (N=4) of startup participants. Startups often 
have unique team structures and resource constraints, leading to 
dierent approaches to addressing UX Design challenges compared 
to established companies. This invites future work to study the 
organizational practices of startup ecosystems, and how GenAI is 
embedded within such structures. Furthermore, although the ma-
jority of our participants had experience using GenAI tools such as 
chatGPT (GPT-3.5) and Midjourney, the study invited participants 
to watch demonstrations of GenAI tools without actual hands-on 
usage. This limited interaction might have overlooked practical 
insights that could arise only from direct hands-on experience with 
such tools. 
7 CONCLUSION 
Our work set out to investigate how UX Designers perceive GenAI 
tools, and how this is reected in their current workows and 
practices. Further, we identied the opportunities and risks do UX 
Designers envision for the future of human-AI collaboration in UX 
Design practice. Through in-depth interviews with 20 UX Designers 
who have diverse years of experience, we found that experienced 
designers are condent in their originality, creativity, and empathic 
skills, and nd GenAI’s role overall as assistive. They emphasized 
factors of “enjoyment” and “agency” as uniquely humans, where 
humans will always remain in the driver seat over AI output. How-
ever, there were serious concerns over setbacks for junior designers, 
who may be impacted by skill degradation, job replacement, and 
creativity exhaustion. We draw several implications for responsi-
ble human-AI collaboration in UX design, specically related to 
copyright and ownership, human creativity, and AI literacy and 
access. We call on continued eorts to develop responsible AI for 
ensuring human and creative safeguarding mechanisms, allowing 
UX Design professionals to immediately yet gracefully adapt to the 
dawn of GenAI, and its disruptive impact on UX Design practice. 
ACKNOWLEDGMENTS 
We thank all our participants for taking part in our study, and 
oering us their valuable perspectives on GenAI. 
REFERENCES 
[1] Abdallah MH Abbas, Khairil Imran Ghauth, and Choo-Yee Ting. 2022. User 
experience design using machine learning: a systematic review. IEEE Access 10 
(2022), 51501–51514.
[2] Saleema Amershi, Dan Weld, Mihaela Vorvoreanu, Adam Fourney, Besmira 
Nushi, Penny Collisson, Jina Suh, Shamsi Iqbal, Paul N. Bennett, Kori Inkpen, 
Jaime Teevan, Ruth Kikin-Gil, and Eric Horvitz. 2019. Guidelines for Human-
AI Interaction. In Proceedings of the 2019 CHI Conference on Human Factors in 
Computing Systems (Glasgow, Scotland Uk) (CHI ’19). Association for Computing 
Machinery, New York, NY, USA, 1–13. https://doi.org/10.1145/3290605.3300233 
[3] Kareem Ayoub and Kenneth Payne. 2016. Strategy in the age of articial 
intelligence. Journal of strategic studies 39, 5-6 (2016), 793–819. 
[4] Emily M. Bender, Timnit Gebru, Angelina McMillan-Major, and Shmargaret 
Shmitchell. 2021. On the Dangers of Stochastic Parrots: Can Language Models 
Be Too Big?. In Proceedings of the 2021 ACM Conference on Fairness, Account-
ability, and Transparency (Virtual Event, Canada) (FAccT ’21). Association for 
Computing Machinery, New York, NY, USA, 610–623. https://doi.org/10.1145/ 
3442188.3445922 
[5] Abeba Birhane, William Isaac, Vinodkumar Prabhakaran, Mark Diaz, 
Madeleine Clare Elish, Iason Gabriel, and Shakir Mohamed. 2022. Power to the 
People? Opportunities and Challenges for Participatory AI. In Equity and Access 
in Algorithms, Mechanisms, and Optimization (Arlington, V A, USA) (EAAMO ’22). 
Association for Computing Machinery, New York, NY, USA, Article 6, 8 pages. 
https://doi.org/10.1145/3551624.3555290 
[6] Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora, 
Sydney von Arx, Michael S. Bernstein, Jeannette Bohg, Antoine Bosselut, Emma 
Brunskill, Erik Brynjolfsson, Shyamal Buch, Dallas Card, Rodrigo Castellon, 
Niladri Chatterji, Annie Chen, Kathleen Creel, Jared Quincy Davis, Dora Dem-
szky, Chris Donahue, Moussa Doumbouya, Esin Durmus, Stefano Ermon, John 
Etchemendy, Kawin Ethayarajh, Li Fei-Fei, Chelsea Finn, Trevor Gale, Lauren 
Gillespie, Karan Goel, Noah Goodman, Shelby Grossman, Neel Guha, Tatsunori 
Hashimoto, Peter Henderson, John Hewitt, Daniel E. Ho, Jenny Hong, Kyle 
Hsu, Jing Huang, Thomas Icard, Saahil Jain, Dan Jurafsky, Pratyusha Kalluri, 
Siddharth Karamcheti, Geo Keeling, Fereshte Khani, Omar Khattab, Pang Wei 
Koh, Mark Krass, Ranjay Krishna, Rohith Kuditipudi, Ananya Kumar, Faisal Lad-
hak, Mina Lee, Tony Lee, Jure Leskovec, Isabelle Levent, Xiang Lisa Li, Xuechen 
Li, Tengyu Ma, Ali Malik, Christopher D. Manning, Suvir Mirchandani, Eric 
Mitchell, Zanele Munyikwa, Suraj Nair, Avanika Narayan, Deepak Narayanan, 
Ben Newman, Allen Nie, Juan Carlos Niebles, Hamed Nilforoshan, Julian Nyarko, 
Giray Ogut, Laurel Orr, Isabel Papadimitriou, Joon Sung Park, Chris Piech, Eva 
Portelance, Christopher Potts, Aditi Raghunathan, Rob Reich, Hongyu Ren, 
Frieda Rong, Yusuf Roohani, Camilo Ruiz, Jack Ryan, Christopher Ré, Dorsa 
Sadigh, Shiori Sagawa, Keshav Santhanam, Andy Shih, Krishnan Srinivasan, 
Alex Tamkin, Rohan Taori, Armin W. Thomas, Florian Tramèr, Rose E. Wang, 
William Wang, Bohan Wu, Jiajun Wu, Yuhuai Wu, Sang Michael Xie, Michihiro 
Yasunaga, Jiaxuan You, Matei Zaharia, Michael Zhang, Tianyi Zhang, Xikun 
Zhang, Yuhui Zhang, Lucia Zheng, Kaitlyn Zhou, and Percy Liang. 2022. On 
the Opportunities and Risks of Foundation Models. arXiv:2108.07258 [cs.LG] 
[7] Zalán Borsos, Raphaël Marinier, Damien Vincent, Eugene Kharitonov, Olivier 
Pietquin, Matt Shari, Olivier Teboul, David Grangier, Marco Tagliasacchi, and 
Neil Zeghidour. 2022. AudioLM: a Language Modeling Approach to Audio 
Generation. arXiv:2209.03143 [cs.SD] 
[8] Petter Bae Brandtzæg, Asbjørn Følstad, and Jan Heim. 2018. Enjoyment: Lessons 
from Karasek. Springer International Publishing, Cham, 331–341. https://doi. 
org/10.1007/978-3-319-68213-6_21 
[9] Virginia Braun and Victoria Clarke. 2012. Thematic analysis. In APA Handbook of 
Research Methods in Psychology: Vol. 2. Research Designs. American Psychological 
Association, 750 First St. NE, Washington, DC 20002-4242, 57–71.

<!-- Page 16 -->

CHI ’24, May 11–16, 2024, Honolulu, HI, USA Li et al. 
[10] Lizzy Burnam. 2023. We Surveyed 1093 Researchers About How They Use 
AI—Here’s What We Learned. https://www.userinterviews.com/blog/ai-in-ux-
research-report 
[11] Patrick Butlin. 2021. AI Alignment and Human Reward. In Proceedings of the 
2021 AAAI/ACM Conference on AI, Ethics, and Society (Virtual Event, USA) 
(AIES ’21). Association for Computing Machinery, New York, NY, USA, 437–445. 
https://doi.org/10.1145/3461702.3462570 
[12] Bill Buxton. 2010. Sketching user experiences: getting the design right and the 
right design. Morgan kaufmann, Burlington, Massachusetts, USA. 
[13] Kelly Caine. 2016. Local Standards for Sample Size at CHI. In Proceedings of 
the 2016 CHI Conference on Human Factors in Computing Systems (San Jose, 
California, USA) (CHI ’16). Association for Computing Machinery, New York, 
NY, USA, 981–992. https://doi.org/10.1145/2858036.2858498 
[14] Tara Capel and Margot Brereton. 2023. What is Human-Centered about Human-
Centered AI? A Map of the Research Landscape. In Proceedings of the 2023 CHI 
Conference on Human Factors in Computing Systems (Hamburg, Germany) (CHI 
’23). Association for Computing Machinery, New York, NY, USA, Article 359, 
23 pages. https://doi.org/10.1145/3544548.3580959 
[15] Minsuk Chang, Stefania Druga, Alexander J. Fiannaca, Pedro Vergani, Chinmay 
Kulkarni, Carrie J Cai, and Michael Terry. 2023. The Prompt Artists. In Proceed-
ings of the 15th Conference on Creativity and Cognition (, Virtual Event, USA,) 
(C&C’23). Association for Computing Machinery, New York, NY, USA, 75–87. 
https://doi.org/10.1145/3591196.3593515 
[16] Li-Yuan Chiou, Peng-Kai Hung, Rung-Huei Liang, and Chun-Teng Wang. 2023.
Designing with AI: An Exploration of Co-Ideation with Image Generators. In 
Proceedings of the 2023 ACM Designing Interactive Systems Conference (Pittsburgh, 
PA, USA) (DIS ’23). Association for Computing Machinery, New York, NY, USA, 
1941–1954. https://doi.org/10.1145/3563657.3596001 
[17] Victoria Clarke, Virginia Braun, and Nikki Hayeld. 2015. Thematic analysis. 
Qualitative psychology: A practical guide to research methods 222, 2015 (2015), 
248. 
[18] Tiago Silva Da Silva, Milene Selbach Silveira, Frank Maurer, and Theodore 
Hellmann. 2012. User experience design and agile development: From theory to 
practice. Journal of Software Engineering and Applications 5, 10 (2012), 743–751. 
https://doi.org/10.4236/jsea.2012.510087 
[19] Smit Desai, Tanusree Sharma, and Pratyasha Saha. 2023. Using ChatGPT in HCI 
Research—A Trioethnography. In Proceedings of the 5th International Conference 
on Conversational User Interfaces (Eindhoven, Netherlands) (CUI ’23). Association 
for Computing Machinery, New York, NY, USA, Article 8, 6 pages. https: 
//doi.org/10.1145/3571884.3603755 
[20] Fiona Draxler, Anna Werner, Florian Lehmann, Matthias Hoppe, Albrecht 
Schmidt, Daniel Buschek, and Robin Welsch. 2024. The AI Ghostwriter Eect: 
When Users do not Perceive Ownership of AI-Generated Text but Self-Declare 
as Authors. ACM Transactions on Computer-Human Interaction 31, 2 (Feb. 2024), 
1–40. https://doi.org/10.1145/3637875 
[21] Upol Ehsan and Mark O. Riedl. 2020. Human-Centered Explainable AI: Towards 
a Reective Sociotechnical Approach. In HCI International 2020 - Late Breaking 
Papers: Multimodality and Intelligence, Constantine Stephanidis, Masaaki Kurosu, 
Helmut Degen, and Lauren Reinerman-Jones (Eds.). Springer International 
Publishing, Cham, 449–466. 
[22] Damian Okaibedi Eke. 2023. ChatGPT and the rise of generative AI: Threat to 
academic integrity? Journal of Responsible Technology 13 (2023), 100060. 
[23] Tyna Eloundou, Sam Manning, Pamela Mishkin, and Daniel Rock. 2023. GPTs 
are GPTs: An Early Look at the Labor Market Impact Potential of Large Language 
Models. arXiv:2303.10130 [econ.GN] 
[24] Chris Elsden, Arthi Manohar, Jo Briggs, Mike Harding, Chris Speed, and John 
Vines. 2018. Making Sense of Blockchain Applications: A Typology for HCI. In 
Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems 
(Montreal QC, Canada) (CHI ’18). Association for Computing Machinery, New 
York, NY, USA, 1–14. https://doi.org/10.1145/3173574.3174032 
[25] Ziv Epstein, Aaron Hertzmann, Investigators of Human Creativity, Memo Akten, 
Hany Farid, Jessica Fjeld, Morgan R Frank, Matthew Groh, Laura Herman, Neil 
Leach, et al. 2023. Art and the science of generative AI. Science 380, 6650 (2023), 
1110–1111. 
[26] Rosanna Fanni, Valerie Steinkogler, Giulia Zampedri, and Jo Pierson. 2022. 
Enhancing human agency through redress in Articial Intelligence Systems. AI 
& SOCIETY 38 (06 2022). https://doi.org/10.1007/s00146-022-01454-7 
[27] Ed Felten, Manav Raj, and Robert Seamans. 2023. How will Language Modelers 
like ChatGPT Aect Occupations and Industries? arXiv:2303.01157 [econ.GN] 
[28] K. J. Kevin Feng, Maxwell James Coppock, and David W. McDonald. 2023. How 
Do UX Practitioners Communicate AI as a Design Material? Artifacts, Concep-
tions, and Propositions. In Proceedings of the 2023 ACM Designing Interactive 
Systems Conference (, Pittsburgh, PA, USA,) (DIS ’23). Association for Computing 
Machinery, New York, NY, USA, 2263–2280. https://doi.org/10.1145/3563657. 
3596101 
[29] Jennifer Fereday and Eimear Muir-Cochrane. 2006. Demonstrating Rigor 
Using Thematic Analysis: A Hybrid Approach of Inductive and Deduc-
tive Coding and Theme Development. International Journal of Qualitative 
Methods 5, 1 (2006), 80–92. https://doi.org/10.1177/160940690600500107 
arXiv:https://doi.org/10.1177/160940690600500107 
[30] Giorgio Franceschelli and Mirco Musolesi. 2023. Reinforcement Learning for 
Generative AI: State of the Art, Opportunities and Open Research Challenges. 
arXiv:2308.00031 [cs.LG] 
[31] Michael C. Frank. 2023. Bridging the data gap between children and large 
language models. Trends in Cognitive Sciences 27, 11 (2023), 990–992. https: 
//doi.org/10.1016/j.tics.2023.08.007 
[32] Jonas Frich, Lindsay MacDonald Vermeulen, Christian Remy, Michael Mose 
Biskjaer, and Peter Dalsgaard. 2019. Mapping the Landscape of Creativity 
Support Tools in HCI. In Proceedings of the 2019 CHI Conference on Human 
Factors in Computing Systems (Glasgow, Scotland Uk) (CHI ’19). Association 
for Computing Machinery, New York, NY, USA, 1–18. https://doi.org/10.1145/ 
3290605.3300619 
[33] Batya Friedman. 1996. Value-Sensitive Design. Interactions 3, 6 (dec 1996), 16–23. 
https://doi.org/10.1145/242485.242493 
[34] Ozlem Ozmen Garibay, Brent Winslow, Salvatore Andolina, Margherita An-
tona, Anja Bodenschatz, Constantinos Coursaris, Gregory Falco, Stephen M. 
Fiore, Ivan Garibay, Keri Grieman, John C. Havens, Marina Jirotka, Hernisa 
Kacorri, Waldemar Karwowski, Joe Kider, Joseph Konstan, Sean Koon, Mon-
ica Lopez-Gonzalez, Iliana Maifeld-Carucci, Sean McGregor, Gavriel Sal-
vendy, Ben Shneiderman, Constantine Stephanidis, Christina Strobel, Car-
olyn Ten Holter, and Wei Xu. 2023. Six Human-Centered Articial Intel-
ligence Grand Challenges. International Journal of Human Computer Inter-
action 39, 3 (2023), 391–437. https://doi.org/10.1080/10447318.2022.2153320 
arXiv:https://doi.org/10.1080/10447318.2022.2153320 
[35] Frederic Gmeiner, Humphrey Yang, Lining Yao, Kenneth Holstein, and Nikolas 
Martelaro. 2023. Exploring Challenges and Opportunities to Support Designers 
in Learning to Co-create with AI-based Manufacturing Design Tools. In Pro-
ceedings of the 2023 CHI Conference on Human Factors in Computing Systems 
(<conf-loc>, <city>Hamburg</city>, <country>Germany</country>, </conf-
loc>) (CHI ’23). Association for Computing Machinery, New York, NY, USA, 
Article 226, 20 pages. https://doi.org/10.1145/3544548.3580999 
[36] Abid Haleem, Mohd Javaid, and Ravi Pratap Singh. 2022. An era of ChatGPT as a 
signicant futuristic support tool: A study on features, abilities, and challenges. 
BenchCouncil Transactions on Benchmarks, Standards and Evaluations 2, 4 (2022), 
100089. https://doi.org/10.1016/j.tbench.2023.100089 
[37] Perttu Hämäläinen, Mikke Tavast, and Anton Kunnari. 2023. Evaluating Large 
Language Models in Generating Synthetic HCI Research Data: a Case Study. In 
Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems 
(<conf-loc>, <city>Hamburg</city>, <country>Germany</country>, </conf-
loc>) (CHI ’23). Association for Computing Machinery, New York, NY, USA, 
Article 433, 19 pages. https://doi.org/10.1145/3544548.3580688 
[38] Ariel Han and Zhenyao Cai. 2023. Design Implications of Generative AI Systems 
for Visual Storytelling for Young Learners. In Proceedings of the 22nd Annual 
ACM Interaction Design and Children Conference (Chicago, IL, USA) (IDC ’23). 
Association for Computing Machinery, New York, NY, USA, 470–474. https: 
//doi.org/10.1145/3585088.3593867 
[39] Gunnar Harboe and Elaine M. Huang. 2015. Real-World Anity Diagramming 
Practices: Bridging the Paper-Digital Gap. In Proceedings of the 33rd Annual 
ACM Conference on Human Factors in Computing Systems (Seoul, Republic of 
Korea) (CHI ’15). Association for Computing Machinery, New York, NY, USA, 
95–104. https://doi.org/10.1145/2702123.2702561 
[40] Rex Hartson and Pardha Pyla. 2018. The UX Book: Process and Guidelines for 
Ensuring a Quality User Experience (2st ed.). Morgan Kaufmann Publishers Inc., 
San Francisco, CA, USA. 
[41] Monique Hennink and Bonnie N. Kaiser. 2022. Sample sizes for saturation in 
qualitative research: A systematic review of empirical tests. Social Science & 
Medicine 292 (2022), 114523. https://doi.org/10.1016/j.socscimed.2021.114523 
[42] Jonathan Ho, William Chan, Chitwan Saharia, Jay Whang, Ruiqi Gao, Alexey 
Gritsenko, Diederik P. Kingma, Ben Poole, Mohammad Norouzi, David J. Fleet, 
and Tim Salimans. 2022. Imagen Video: High Denition Video Generation with 
Diusion Models. arXiv:2210.02303 [cs.CV] 
[43] Matthew K. Hong, Shabnam Hakimi, Yan-Ying Chen, Heishiro Toyoda, Charlene 
Wu, and Matt Klenk. 2023. Generative AI for Product Design: Getting the Right 
Design and the Design Right. arXiv:2306.01217 [cs.HC] 
[44] Eric Horvitz. 1999. Principles of mixed-initiative user interfaces. In Proceedings 
of the SIGCHI Conference on Human Factors in Computing Systems (Pittsburgh, 
Pennsylvania, USA) (CHI ’99). Association for Computing Machinery, New York, 
NY, USA, 159–166. https://doi.org/10.1145/302979.303030 
[45] Stephanie Houde, Steven I Ross, Michael Muller, Mayank Agarwal, Fernando 
Martinez, John Richards, Kartik Talamadupula, and Justin D Weisz. 2022. Oppor-
tunities for Generative AI in UX Modernization. In Joint Proceedings of the ACM 
IUI Workshops 2022, March 2022, Helsinki, Finland. Association for Computing 
Machinery, New York, NY, USA. 
[46] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian 
Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, and Ting 
Liu. 2023. A Survey on Hallucination in Large Language Models: Principles,

<!-- Page 17 -->

User Experience Design Professionals’ Perceptions of Generative AI CHI ’24, May 11–16, 2024, Honolulu, HI, USA 
Taxonomy, Challenges, and Open Questions. arXiv:2311.05232 [cs.CL] 
[47] Nanna Inie, Jeanette Falk, and Steve Tanimoto. 2023. Designing Participatory 
AI: Creative Professionals’ Worries and Expectations about Generative AI. In 
Extended Abstracts of the 2023 CHI Conference on Human Factors in Computing 
Systems (<conf-loc>, <city>Hamburg</city>, <country>Germany</country>, 
</conf-loc>) (CHI EA ’23). Association for Computing Machinery, New York, 
NY, USA, Article 82, 8 pages. https://doi.org/10.1145/3544549.3585657 
[48] Alice M Isen and Johnmarshall Reeve. 2005. The inuence of positive aect on 
intrinsic and extrinsic motivation: Facilitating enjoyment of play, responsible 
work behavior, and self-control. Motivation and emotion 29 (2005), 295–323. 
[49] Maurice Jakesch, Zana Buçinca, Saleema Amershi, and Alexandra Olteanu. 2022. 
How Dierent Groups Prioritize Ethical Values for Responsible AI. In Proceedings 
of the 2022 ACM Conference on Fairness, Accountability, and Transparency (Seoul, 
Republic of Korea) (FAccT ’22). Association for Computing Machinery, New 
York, NY, USA, 310–323. https://doi.org/10.1145/3531146.3533097 
[50] Harry H. Jiang, Lauren Brown, Jessica Cheng, Mehtab Khan, Abhishek Gupta, 
Deja Workman, Alex Hanna, Johnathan Flowers, and Timnit Gebru. 2023. AI 
Art and Its Impact on Artists. In Proceedings of the 2023 AAAI/ACM Conference 
on AI, Ethics, and Society (Montréal, QC, Canada) (AIES ’23). Association for 
Computing Machinery, New York, NY, USA, 363–374. https://doi.org/10.1145/ 
3600211.3604681 
[51] Zachary Kaiser. 2019. Creativity as computation: Teaching design in the age of 
automation. Design and Culture 11, 2 (2019), 173–192. 
[52] Taenyun Kim, Maria D Molina, Minjin Rheu, Emily S Zhan, and Wei Peng. 2023.
One AI Does Not Fit All: A Cluster Analysis of the Laypeople’s Perception of AI 
Roles. In Proceedings of the 2023 CHI Conference on Human Factors in Computing 
Systems (CHI ’23). Association for Computing Machinery, New York, NY, USA, 
Article 29, 1–20 pages. https://doi.org/10.1145/3544548.3581340 
[53] Joke Kort, APOS Vermeeren, and Jenneke E Fokker. 2007. Conceptualizing and 
measuring user experience. , 57–64 pages. 
[54] Thomas S. Kuhn. 1962. The Structure of Scientic Revolutions. University of 
Chicago Press, Chicago. 
[55] Chinmay Kulkarni, Stefania Druga, Minsuk Chang, Alex Fiannaca, Carrie Cai, 
and Michael Terry. 2023. A Word is Worth a Thousand Pictures: Prompts as AI 
Design Material. arXiv:2303.12647 [cs.HC] 
[56] Tomas Lawton, Kazjon Grace, and Francisco J Ibarrola. 2023. When is a Tool a 
Tool? User Perceptions of System Agency in Human–AI Co-Creative Drawing. In 
Proceedings of the 2023 ACM Designing Interactive Systems Conference (Pittsburgh, 
PA, USA) (DIS ’23). Association for Computing Machinery, New York, NY, USA, 
1978–1996. https://doi.org/10.1145/3563657.3595977 
[57] Mina Lee, Megha Srivastava, Amelia Hardy, John Thickstun, Esin Durmus, 
Ashwin Paranjape, Ines Gerard-Ursin, Xiang Lisa Li, Faisal Ladhak, Frieda Rong, 
Rose E. Wang, Minae Kwon, Joon Sung Park, Hancheng Cao, Tony Lee, Rishi 
Bommasani, Michael Bernstein, and Percy Liang. 2024. Evaluating Human-
Language Model Interaction. arXiv:2212.09746 [cs.CL] 
[58] Florian Lehmann. 2023. Mixed-Initiative Interaction with Computational Gener-
ative Systems. In Extended Abstracts of the 2023 CHI Conference on Human 
Factors in Computing Systems (Hamburg, Germany) (CHI EA ’23). Associa-
tion for Computing Machinery, New York, NY, USA, Article 501, 6 pages. 
https://doi.org/10.1145/3544549.3577061 
[59] Robert W Lent and Steven D Brown. 2006. Integrating person and situation 
perspectives on work satisfaction: A social-cognitive view. Journal of vocational 
behavior 69, 2 (2006), 236–247. 
[60] Joseph CR Licklider. 1960. Man-Computer Symbiosis. IRE Transactions on 
Human Factors in Electronics HFE-1, 1 (1960), 4–11. 
[61] Lassi A. Liikkanen. 2019. It AIn’t Nuttin’ New – Interaction Design Practice 
After the AI Hype. In Human-Computer Interaction – INTERACT 2019, David 
Lamas, Fernando Loizides, Lennart Nacke, Helen Petrie, Marco Winckler, and 
Panayiotis Zaphiris (Eds.). Springer International Publishing, Cham, 600–604. 
[62] Zhiyu Lin, Upol Ehsan, Rohan Agarwal, Samihan Dani, Vidushi Vashishth, and 
Mark Riedl. 2023. Beyond Prompts: Exploring the Design Space of Mixed-
Initiative Co-Creativity Systems. arXiv:2305.07465 [cs.AI] 
[63] Duri Long and Brian Magerko. 2020. What is AI Literacy? Competencies and 
Design Considerations. In Proceedings of the 2020 CHI Conference on Human 
Factors in Computing Systems (Honolulu, HI, USA) (CHI ’20). Association for 
Computing Machinery, New York, NY, USA, 1–16. https://doi.org/10.1145/ 
3313831.3376727 
[64] Robyn Longhurst. 2003. Semi-structured interviews and focus groups. Key 
methods in geography 3, 2 (2003), 143–156. 
[65] Yuwen Lu, Chengzhi Zhang, Iris Zhang, and Toby Jia-Jun Li. 2022. Bridging 
the Gap Between UX Practitioners’ Work Practices and AI-Enabled Design 
Support Tools. In Extended Abstracts of the 2022 CHI Conference on Human 
Factors in Computing Systems (New Orleans, LA, USA) (CHI EA ’22). Association 
for Computing Machinery, New York, NY, USA, Article 268, 7 pages. https: 
//doi.org/10.1145/3491101.3519809 
[66] Henrietta Lyons, Eduardo Velloso, and Tim Miller. 2021. Conceptualising Con-
testability: Perspectives on Contesting Algorithmic Decisions. Proc. ACM 
Hum.-Comput. Interact. 5, CSCW1, Article 106 (apr 2021), 25 pages. https: 
//doi.org/10.1145/3449180 
[67] Nora McDonald, Sarita Schoenebeck, and Andrea Forte. 2019. Reliability and 
Inter-rater Reliability in Qualitative Research: Norms and Guidelines for CSCW 
and HCI Practice. Proceedings of the ACM on Human-Computer Interaction 3 (11 
2019), 1–23. https://doi.org/10.1145/3359174 
[68] Kobe Millet, Florian Buehler, Guanzhong Du, and Michail D. Kokkoris. 2023. 
Defending humankind: Anthropocentric bias in the appreciation of AI art. 
Computers in Human Behavior 143 (2023), 107707. https://doi.org/10.1016/ 
j.chb.2023.107707 
[69] Bin Ning, Fang Liu, and Zhixiong Liu. 2023. Creativity Support in AI Co-creative 
Tools: Current Research, Challenges and Opportunities. In 2023 26th Interna-
tional Conference on Computer Supported Cooperative Work in Design (CSCWD). 
IEEE, New York, NY, USA, 5–10. https://doi.org/10.1109/CSCWD57460.2023. 
10152832 
[70] Lorelli S. Nowell, Jill M. Norris, Deborah E. White, and Nancy J. Moules. 2017. 
Thematic Analysis: Striving to Meet the Trustworthiness Criteria. International 
Journal of Qualitative Methods 16, 1 (2017), 1609406917733847. https://doi.org/ 
10.1177/1609406917733847 arXiv:https://doi.org/10.1177/1609406917733847 
[71] Shakked Noy and Whitney Zhang. 2023. Experimental evidence on the produc-
tivity eects of generative articial intelligence. A vailable at SSRN 4375283 381, 
6654 (2023), 187–192. https://doi.org/10.1126/science.adh2586 
[72] OpenAI, Josh Achiam, Steven Adler, and Sandhini Agarwal et al. 2023. GPT-4 
Technical Report. arXiv:2303.08774 [cs.CL] 
[73] Antti Oulasvirta, Niraj Ramesh Dayama, Morteza Shiripour, Maximilian John,
and Andreas Karrenbauer. 2020. Combinatorial optimization of graphical user 
interface designs. Proc. IEEE 108, 3 (2020), 434–464. 
[74] Joon Sung Park, Lindsay Popowski, Carrie Cai, Meredith Ringel Morris, Percy 
Liang, and Michael S. Bernstein. 2022. Social Simulacra: Creating Populated 
Prototypes for Social Computing Systems. In Proceedings of the 35th Annual 
ACM Symposium on User Interface Software and Technology (Bend, OR, USA) 
(UIST ’22). Association for Computing Machinery, New York, NY, USA, Article 
74, 18 pages. https://doi.org/10.1145/3526113.3545616 
[75] John V Pavlik. 2023. Collaborating with ChatGPT: Considering the implica-
tions of generative articial intelligence for journalism and media education. 
Journalism & Mass Communication Educator78, 1 (2023), 84–93. 
[76] Andrew Pearson. 2023. The rise of CreAltives: Using AI to enable and speed up 
the creative process. Journal of AI, Robotics & Workplace Automation 2, 2 (2023), 
101–114. 
[77] Sida Peng, Eirini Kalliamvakou, Peter Cihon, and Mert Demirer. 2023. The 
Impact of AI on Developer Productivity: Evidence from GitHub Copilot. 
arXiv:2302.06590 [cs.SE] 
[78] Bogdana Rakova, Jingying Yang, Henriette Cramer, and Rumman Chowdhury. 
2021. Where Responsible AI Meets Reality: Practitioner Perspectives on Enablers 
for Shifting Organizational Practices. Proc. ACM Hum.-Comput. Interact. 5, 
CSCW1, Article 7 (apr 2021), 23 pages. https://doi.org/10.1145/3449081 
[79] Kevin Roose. 2022. The brilliance and weirdness of ChatGPT. https://www. 
nytimes.com/2022/12/05/technology/chatgpt-ai-twitter.html 
[80] S. Russell. 2019. Human Compatible: Articial Intelligence and the Problem of 
Control. Penguin Publishing Group, New York, NY, USA. https://books.google. 
nl/books?id=M1eFDwAAQBAJ 
[81] Jana I Saadi and Maria C Yang. 2023. Generative Design: Reframing the Role of 
the Designer in Early-Stage Design Process. Journal of Mechanical Design 145, 
4 (2023), 041411. 
[82] Chitwan Saharia, William Chan, Saurabh Saxena, Lala Li, Jay Whang, Emily L 
Denton, Kamyar Ghasemipour, Raphael Gontijo Lopes, Burcu Karagol Ayan, Tim 
Salimans, et al. 2022. Photorealistic text-to-image diusion models with deep 
language understanding. Advances in Neural Information Processing Systems 35 
(2022), 36479–36494. 
[83] NANNA SANDBERG, TOM HOY, and MARTIN ORTLIEB. 2019. My AI versus 
the company AI: how knowledge workers conceptualize forms of AI assistance 
in the workplace. In Ethnographic Praxis in Industry Conference Proceedings, 
Vol. 2019. Wiley Online Library, American Anthropological Association, Arling-
ton, Virginia, USA, 125–143. 
[84] Ava Elizabeth Scott, Daniel Neumann, Jasmin Niess, and Paweł W. Woźniak. 
2023. Do You Mind? User Perceptions of Machine Consciousness. In Proceedings 
of the 2023 CHI Conference on Human Factors in Computing Systems (<conf-loc>, 
<city>Hamburg</city>, <country>Germany</country>, </conf-loc>) (CHI ’23). 
Association for Computing Machinery, New York, NY, USA, Article 374, 19 pages. 
https://doi.org/10.1145/3544548.3581296 
[85] Ben Shneiderman. 2020. Human-centered articial intelligence: Reliable, safe & 
trustworthy. International Journal of Human–Computer Interaction 36, 6 (2020), 
495–504. 
[86] Ben Shneiderman. 2020. Human-centered articial intelligence: Three fresh 
ideas. AIS Transactions on Human-Computer Interaction 12, 3 (2020), 109–124. 
[87] D.K. Simonton. 1999. Origins of Genius: Darwinian Perspectives on Creativ-
ity. Oxford University Press, Oxford, UK. https://books.google.li/books?id= 
a2LnBwAAQBAJ

<!-- Page 18 -->

CHI ’24, May 11–16, 2024, Honolulu, HI, USA Li et al. 
[88] Marita Skjuve, Asbjørn Følstad, and Petter Bae Brandtzaeg. 2023. The User 
Experience of ChatGPT: Findings from a Questionnaire Study of Early Users. In 
Proceedings of the 5th International Conference on Conversational User Interfaces 
(Eindhoven, Netherlands) (CUI ’23). Association for Computing Machinery, New 
York, NY, USA, Article 2, 10 pages. https://doi.org/10.1145/3571884.3597144 
[89] Irene Solaiman, Zeerak Talat, William Agnew, Lama Ahmad, Dylan Baker, 
Su Lin Blodgett, Hal Daumé III au2, Jesse Dodge, Ellie Evans, Sara Hooker, 
Yacine Jernite, Alexandra Sasha Luccioni, Alberto Lusoli, Margaret Mitchell, 
Jessica Newman, Marie-Therese Png, Andrew Strait, and Apostol Vassilev. 2023. 
Evaluating the Social Impact of Generative AI Systems in Systems and Society. 
arXiv:2306.05949 [cs.CY] 
[90] Åsne Stige, Efpraxia D Zamani, Patrick Mikalef, and Yuzhen Zhu. 2023. Articial 
intelligence (AI) for user experience (UX) design: a systematic literature review 
and future research agenda. https://doi.org/10.1108/ITP-07-2022-0519 
[91] S Shyam Sundar. 2020. Rise of machine agency: A framework for studying the 
psychology of human–AI interaction (HAII). Journal of Computer-Mediated 
Communication 25, 1 (2020), 74–88. 
[92] Jakob Tholander and Martin Jonsson. 2023. Design Ideation with AI - Sketching, 
Thinking and Talking with Generative Machine Learning Models. In Proceedings 
of the 2023 ACM Designing Interactive Systems Conference (Pittsburgh, PA, USA) 
(DIS ’23). Association for Computing Machinery, New York, NY, USA, 1930–1940. 
https://doi.org/10.1145/3563657.3596014 
[93] Katja Thoring, Sebastian Huettemann, and Roland M Mueller. 2023. THE 
AUGMENTED DESIGNER: A RESEARCH AGENDA FOR GENERATIVE AI-
ENABLED DESIGN. Proceedings of the Design Society 3 (2023), 3345–3354. 
[94] Joel E Tohline et al. 2008. Computational provenance. Computing in Science & 
Engineering 10, 03 (2008), 9–10. 
[95] Steven Umbrello and Ibo Poel. 2021. Mapping value sensitive design onto AI 
for social good principles. AI and Ethics 1 (08 2021), 3. https://doi.org/10.1007/ 
s43681-021-00038-3 
[96] Russ Unger and Carolyn Chandler. 2012. A Project Guide to UX Design: For user 
experience designers in the eld or in the making. New Riders, Nora, Indianapolis, 
USA. 
[97] Michael Veale and Frederik Zuiderveen Borgesius. 2021. Demystifying the Draft 
EU Articial Intelligence Act — Analysing the good, the bad, and the unclear 
elements of the proposed approach. Computer Law Review International 22, 4 
(Aug. 2021), 97–112. https://doi.org/10.9785/cri-2021-220402 
[98] Florent Vinchon, Todd Lubart, Sabrina Bartolotta, Valentin Gironnay, Marion 
Botella, Samira Bourgeois-Bougrine, Jean-Marie Burkhardt, Nathalie Bonnardel, 
Giovanni Emanuele Corazza, Vlad Glăveanu, et al. 2023. Articial Intelligence 
& Creativity: A manifesto for collaboration. The Journal of Creative Behavior 
57, 4 (2023), 472–484. 
[99] Qian Wan and Zhicong Lu. 2023. GANCollage: A GAN-Driven Digital Mood 
Board to Facilitate Ideation in Creativity Support. In Proceedings of the 2023 
ACM Designing Interactive Systems Conference (Pittsburgh, PA, USA) (DIS ’23). 
Association for Computing Machinery, New York, NY, USA, 136–146. https: 
//doi.org/10.1145/3563657.3596072 
[100] Norbert Wiener. 1960. Some Moral and Technical Consequences of Automation. 
Science 131, 3410 (1960), 1355–1358. https://doi.org/10.1126/science.131.3410. 
1355 arXiv:https://www.science.org/doi/pdf/10.1126/science.131.3410.1355 
[101] Wen Xu and Katina Zammit. 2020. Applying Thematic Analysis to Education: 
A Hybrid Approach to Interpreting Data in Practitioner Research. International 
Journal of Qualitative Methods 19 (2020), 1609406920918810. https://doi.org/10. 
1177/1609406920918810 arXiv:https://doi.org/10.1177/1609406920918810 
[102] Bin Yang, Long Wei, and Zihan Pu. 2020. Measuring and improving user expe-
rience through articial intelligence-aided design. Frontiers in Psychology 11 
(2020), 595374. 
[103] Qian Yang, Aaron Steinfeld, Carolyn Rosé, and John Zimmerman. 2020. Re-
examining Whether, Why, and How Human-AI Interaction Is Uniquely Dif-
cult to Design. In Proceedings of the 2020 CHI Conference on Human Factors 
in Computing Systems (<conf-loc>, <city>Honolulu</city>, <state>HI</state>, 
<country>USA</country>, </conf-loc>) (CHI ’20). Association for Computing 
Machinery, New York, NY, USA, 1–13. https://doi.org/10.1145/3313831.3376301 
[104] Yang Yuan. 2023. On the Power of Foundation Models. In Proceedings of the 40th 
International Conference on Machine Learning (Proceedings of Machine Learning 
Research, Vol. 202), Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara 
Engelhardt, Sivan Sabato, and Jonathan Scarlett (Eds.). PMLR, USA, 40519–40530. 
https://proceedings.mlr.press/v202/yuan23b.html 
[105] Xiao Zhan, Yifan Xu, and Stefan Sarkadi. 2023. Deceptive AI Ecosystems: 
The Case of ChatGPT. In Proceedings of the 5th International Conference on 
Conversational User Interfaces (Eindhoven, Netherlands) (CUI ’23). Association 
for Computing Machinery, New York, NY, USA, Article 3, 6 pages. https: 
//doi.org/10.1145/3571884.3603754 
[106] Chengzhi Zhang, Weijie Wang, Paul Pangaro, Nikolas Martelaro, and Daragh 
Byrne. 2023. Generative Image AI Using Design Sketches as Input: Opportunities 
and Challenges. In Proceedings of the 15th Conference on Creativity and Cognition 
(Virtual Event, USA) (C&C ’23). Association for Computing Machinery, New 
York, NY, USA, 254–261. https://doi.org/10.1145/3591196.3596820 
[107] Haonan Zhong, Jiamin Chang, Ziyue Yang, Tingmin Wu, Pathum Chamikara 
Mahawaga Arachchige, Chehara Pathmabandu, and Minhui Xue. 2023. Copy-
right Protection and Accountability of Generative AI: Attack, Watermarking and 
Attribution. In Companion Proceedings of the ACM Web Conference 2023 (Austin, 
TX, USA) (WWW ’23 Companion). Association for Computing Machinery, New 
York, NY, USA, 94–98. https://doi.org/10.1145/3543873.3587321 
[108] Simon Zhuang and Dylan Hadeld-Menell. 2020. Consequences of Misaligned 
AI. In Advances in Neural Information Processing Systems, H. Larochelle, M. Ran-
zato, R. Hadsell, M.F. Balcan, and H. Lin (Eds.), Vol. 33. Curran Associates, Inc., 
Red Hook, New York, USA, 15763–15773.