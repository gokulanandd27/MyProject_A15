import re
from transformers import pipeline

class ToxicityDetector:
    def __init__(self):
        # 1. Keyword Lists by Severity
        
        # Medium Severity: Insults, mild toxicity
        self.medium_severity_keywords = [
            "stupid", "idiot", "dumb", "bad", "terrible", "worst", "ugly", "fat",
            "crazy", "mad", "fool", "loser", "jerk", "creep", "trash", "scum",
            "useless", "nonsense", "rubbish", "fake", "liar", "clown", "noob",
            "bot", "npc", "weirdo", "sucker", "moron", "imbecile", "dimwit",
            "tool", "bonehead", "airhead", "lame", "suck", "annoying", "shut up",
            "gross", "disgusting", "pathetic", "weak", "scrub", "failure",
            

            # Tamil (Medium)
            "muttal", "muttaal", "muttal paiya", "naaye", "poda", "podi", "loosu", 
            "loosu paiya", "kevalam", "paithiyam", "paithiyakaran", "paithiyakari", 
            "settai", "summa po", "pethaiyan", "pethaiyi", "nee ozhungillai", 
            "ozhungillathavan", "ozhungillathaval", "thalaila sariyillai", 
            "muttal maari", "mokkai", "mokkai pannathe", "poiyyan", "poiyyi", 
            "kazhudhai", "erumai", "moodan", "moodathanam",
            # Tamil Set 2 (Medium)
            "madaiyan", "madaiyi", "madathanam", "mandai", "mandaiyillathavan", 
            "moolai illathavan", "moolai illathaval", "aruvaruppu", "aruvaruppanavan", 
            "aruvaruppanaval", "kevalamanavan", "kevalamanaval", "asingam", 
            "asingamanavan", "asingamanaval", "payale", "payalu", "porukki", 
            "porukki paiya", "tharithiram", "tharithiran", "tharithiri", 
            "kevalakaran", "kevalakari", "summa iru da", "mookkillathavan", 
            "konjam arivu iru", "arivillathavan", "arivillathaval", "ada naaye", 
            "kedu", "ketta manushan", "ketta manushi", "kodiyavan", "kodiyaval", 
            "pei maari", "somberi", "somberithanam", "pazhi", "azhukku", 
            "azhukkanavan", "azhukkanaval",
            
            # Tamil Script (Medium)
            "முட்டாள்", "முட்டாள் பையா", "நாயே", "போடா", "போடி", "லூசு", "கேவலம்", 
            "பைத்தியம்", "பைத்தியக்காரன்", "பைத்தியக்காரி", "சேட்டை", "சும்மா போ", 
            "பேதையன்", "பேதையி", "நீ ஒழுங்கில்லை", "ஒழுங்கில்லாதவன்", "ஒழுங்கில்லாதவள்", 
            "தலைல சரியில்லை", "முட்டாள் மாதிரி", "மொக்கை", "மொக்கை பண்ணாதே", 
            "பொய்யன்", "பொய்யி", "கழுதை", "எருமை", "மூடன்", "மூடத்தனம்",
            # Tamil Script Set 2 (Medium)
            "மடையன்", "மடையி", "மடையன் மாதிரி", "மடத்தனம்", "மண்டை", 
            "மண்டைய உடைஞ்சவன்", "மண்டையில்லாதவன்", "மூளை இல்லாதவன்", "மூளை இல்லாதவள்", 
            "அருவருப்பு", "அருவருப்பானவன்", "அருவருப்பானவள்", "கேவலமானவன்", 
            "கேவலமானவள்", "அசிங்கம்", "அசிங்கமானவன்", "அசிங்கமானவள்", "பயலே", 
            "பயலு", "பொறுக்கி", "பொறுக்கி பையா", "தரித்திரம்", "தரித்திரன்", 
            "தரித்திரி", "கேவலக்காரன்", "கேவலக்காரி", "சும்மா இரு டா", 
            "மூக்கில்லாதவன்", "கொஞ்சம் அறிவு இரு", "அறிவில்லாதவன்", "அறிவில்லாதவள்", 
            "அட நாயே", "கேடு", "கெட்ட மனுஷன்", "கெட்ட மனுஷி", "கொடியவன்", 
            "கொடியவள்", "பேய் மாதிரி", "சோம்பேறி", "சோம்பேறித்தனம்", "பழி", 
            "அழுக்கு", "அழுக்கானவன்", "அழுக்கானவள்"
        ]
        
        # High Severity: Slurs, hate speech, threats, extreme profanity
        self.high_severity_keywords = [
            # English High Severity
            "hate", "kill", "die", "racist", "sexist", "scam", "fraud",
            "abuse", "threat", "harass", "fuck", "shit", "bitch", "asshole",
            "cunt", "dick", "cock", "pussy", "bastard", "whore", "slut",
            "fag", "faggot", "dyke", "tranny", "nigger", "nigga", "retard",
            "rapist", "pedophile", "pedo", "incest", "suicide", "murder",
            "terrorist", "bomb", "shoot", "stab", "rape", "molest",
            

            
            # Tamil Colloquialisms (High)
            "gomma", "gotha", "punda", "bunda", "kandaroli", "thaiyoli", "sunni", "junni", 
            "thevutu punda", "kena kuthi", "kena punda", "puluthi punda", "kena thaiyoli", 
            "thevidiya punda", "thevidiya sunni", "oombu", "umbu", "kai adicha patti", 
            "kundi", "kuthi", "kotta", "potta", "themutu thaiyoli", "karumunda", "munda", 
            "loosu punda", "loosu bunda", "kiruku theduviya", "ali punda", "ali thaiyoli", 
            "ali munda", "thevidiya munda", "suuthu", "suthu", "gommala", "kiruku", "goya", 
            "goppen", "sotta thaiyoli", "kiruku bumda", "kiruku bunda", "kiruku punda", 
            "kiruku kuthi", "kiruku thaili", "thaili", "thaili munda", "mental bunda", 
            "mental bumda", "mental punda", "mental thaili", "manda thaiyoli", "kunju", 
            "kunji", "kunjan", "poolu", "poola", "othu", "okkamala", "baade",
            
            # Tamil Additional (High)
            "mosadi", "vesham", "ayokkiyan", "ayokkiyi", "vesi", "mosamanavan", 
            "mosamanaval", "kettavan", "kettaval", "sandali", "sandalan", "ketta pechu",
            "mandaya podu",
            # Tamil Script (High)
            "மோசடி", "வேஷம்", "அயோக்கியன்", "அயோக்கியி", "வேசி", "மோசமானவன்", 
            "மோசமானவள்", "கெட்டவன்", "கெட்டவள்", "சண்டாளி", "சண்டாளன்", "கெட்ட பேச்சு",
            "மண்டைய போடு",
            # Tamil Script Set 3 (High - Slurs)
            "கொம்மா", "கோதா", "புண்டா", "புண்டை", "கண்டரோலி", "தாயோலி", "சுன்னி", "ஜுன்னி", 
            "தேவுட்டு புண்டா", "கேண குத்தி", "கேண புண்டா", "புளுதி புண்டா", "கேண தாயோலி", 
            "தேவிடியா புண்டா", "தேவிடியா சுன்னி", "ஊம்பு", "உம்பு", "கை அடிச்ச பட்டி", 
            "குண்டி", "குத்தி", "கொட்டா", "பொட்டா", "தேமுட்டு தாயோலி", "கருமுண்டா", 
            "முண்டா", "லூசு புண்டா", "லூசு புண்டை", "கிறுக்கு தேடுவியா", "அலி புண்டா", 
            "அலி தாயோலி", "அலி முண்டா", "தேவிடியா முண்டா", "சூத்து", "சுத்து", 
            "கொம்மலா", "கிறுக்கு", "கொய்யா", "கொப்பென்", "சொட்ட தாயோலி", 
            "கிறுக்கு புண்டை", "கிறுக்கு புண்டா", "கிறுக்கு குத்தி", "கிறுக்கு தாய்லி", 
            "தாய்லி", "தாய்லி முண்டா", "மென்டல் புண்டை", "மென்டல் புண்டா", 
            "மென்டல் தாய்லி", "மண்ட தாயோலி", "குஞ்சு", "குஞ்சி", "குஞ்சன்", 
            "பூலு", "பூலா", "ஒத்து", "ஒக்கமலா", "பாடே",
            
            # Obfuscated / Leet Speak (assume High for now as they are intentional evasions)
            "pund@", "pu#nda", "pu*nda", "p*nda", "p***a", "bund@", "bu#nda", "bu*nda", 
            "b*nda", "b***a", "thaiy0li", "thaiy@li", "thaiy*li", "tha*yoli", "thevidiy@", 
            "thev!diya", "thev*d!ya", "th*vidiya", "sunn!", "sun#i", "su*ni", "s*nn!", 
            "kunj!", "kunj@", "ku*ji", "k*nju", "kund!", "kund@", "ku*di", "k*ndi",
            "f*ck", "f**k", "sh*t", "sh!t", "b!tch", "b*tch", "a$$hole", "a**hole",
            "n!gga", "n*gga", "n!gger", "n*gger", "r@pist", "p3do", "k!ll", "d!e"
        ]

        # 2. Initialize XLM-RoBERTa Model
        print("Loading XLM-RoBERTa model... This might take a while on first run.")
        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis", 
                model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
                tokenizer="cardiffnlp/twitter-xlm-roberta-base-sentiment"
            )
            print("XLM-RoBERTa model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.sentiment_analyzer = None

        # 3. Emoji Lists
        self.medium_severity_emojis = ["🤮", "🤢", "🤬", "💩", "🤡", "👎", "😤"]
        self.high_severity_emojis = ["🖕", "🖕🏻", "🖕🏼", "🖕🏽", "🖕🏾", "🖕🏿"]
        
    def predict(self, text):
        """
        Analyze the text using Hybrid Approach (Keywords + XLM-RoBERTa).
        Returns prediction with Severity Levels (High, Medium, Low).
        """
        # Normalize text: lowercase
        text_lower = text.lower()
        
        # --- Step 0: Emoji Check (Direct Substring) ---
        for emoji in self.high_severity_emojis:
            if emoji in text:
                 return {
                    "message_type": "toxic",
                    "display_text": text,
                    "warning_text": "Message removed: High Severity - Contains toxic emojis",
                    "action": "warn",
                    "duration": "7 seconds",
                    "reason": "Contains toxic emojis",
                    "severity": "High"
                }

        for emoji in self.medium_severity_emojis:
            if emoji in text:
                 return {
                    "message_type": "toxic",
                    "display_text": text,
                    "warning_text": "Message removed: Medium Severity - Contains toxic emojis",
                    "action": "warn",
                    "duration": "7 seconds",
                    "reason": "Contains toxic emojis",
                    "severity": "Medium"
                }

        # --- Step 1: Fast Keyword Check ---
        
        # Check High Severity First
        for word in self.high_severity_keywords:
            if re.match(r'^[a-z0-9\s]+$', word):
                pattern = re.compile(r'\b' + re.escape(word) + r'\b')
                match = pattern.search(text_lower)
            else:
                match = word in text_lower
                
            if match:
                return {
                    "message_type": "toxic",
                    "display_text": text,
                    "warning_text": "Message removed: High Severity - Contains banned words/slurs",
                    "action": "warn",
                    "duration": "7 seconds",
                    "reason": "Contains banned words/slurs",
                    "severity": "High"
                }

        # Check Medium Severity
        for word in self.medium_severity_keywords:
            if re.match(r'^[a-z0-9\s]+$', word):
                pattern = re.compile(r'\b' + re.escape(word) + r'\b')
                match = pattern.search(text_lower)
            else:
                match = word in text_lower
                
            if match:
                return {
                    "message_type": "toxic",
                    "display_text": text,
                    "warning_text": "Message removed: Medium Severity - Contains insults/profanity",
                    "action": "warn",
                    "duration": "7 seconds",
                    "reason": "Contains insults/profanity",
                    "severity": "Medium"
                }
            
        # --- Step 2: XLM-RoBERTa Model Check ---
        if self.sentiment_analyzer:
            try:
                results = self.sentiment_analyzer(text)
                label = results[0]['label']
                score = results[0]['score']
                
                # Treat 'negative' with high confidence as toxic
                if label == 'negative':
                    severity = "Low"
                    reason_text = "Flagged for negative sentiment"
                    
                    if score > 0.90:
                        severity = "High"
                        reason_text = "Detected as highly toxic/hateful"
                    elif score > 0.80:
                        severity = "Medium"
                        reason_text = "Detected as potentially harmful"
                    elif score > 0.70:
                        severity = "Low"
                        reason_text = "Flagged for negative sentiment"
                    else:
                        # Below 0.70 confidence, we consider it safe/neutral for now
                        return {
                            "message_type": "non-toxic",
                            "display_text": text,
                            "action": "show",
                            "duration": "permanent"
                        }

                    return {
                        "message_type": "toxic",
                        "display_text": text,
                        "warning_text": f"Message removed: {severity} Severity - {reason_text}",
                        "action": "warn",
                        "duration": "7 seconds",
                        "reason": reason_text,
                        "severity": severity
                    }
                    
            except Exception as e:
                print(f"Model inference failed: {e}")
                
        # --- Step 3: Safe ---
        return {
            "message_type": "non-toxic",
            "display_text": text,
            "action": "show",
            "duration": "permanent"
        }
