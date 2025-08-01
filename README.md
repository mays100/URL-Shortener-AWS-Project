מקצר כתובות פשוט באמצעות AWS Lambda, DynamoDB ו-S3
פרויקט זה מציג מקצר כתובות מינימליסטי ו-serverless הבנוי על שירותי Amazon Web Services (AWS). הוא מאפשר למשתמשים לקצר כתובות URL ארוכות ולקבל קישור קצר המפנה לכתובת המקורית.

מטרות הפרויקט
מקצר כתובות serverless: פונקציונליות הליבה ממומשת באמצעות AWS Lambda ו-DynamoDB.

Frontend סטטי: ממשק המשתמש (UI) מתארח כאתר סטטי ב-AWS S3.

הפניה ישירה: קישורים מקוצרים מפנים ישירות לכתובות ה-URL המקוריות.

ארכיטקטורה
Frontend: קובץ index.html סטטי עם JavaScript, מתארח ב-AWS S3.

Backend: פונקציית AWS Lambda ב-Python, חשופה באמצעות Lambda Function URL.

Database: טבלת DynamoDB בשם ShortUrls לאחסון מיפויי ה-ID הקצר ל-URL המקורי.

מדריך התקנה ופריסה שלב אחר שלב
בצע את השלבים הבאים כדי להקים את מקצר הכתובות שלך ב-AWS.

שלב 1: יצירת טבלת DynamoDB
DynamoDB תשמש לאחסון הקישורים המקוצרים וה-URL המקוריים שלהם.

התחבר לקונסולת AWS: נווט לקונסולת AWS (https://aws.amazon.com/console/).

עבור ל-DynamoDB: חפש "DynamoDB" בסרגל החיפוש ובחר בו.

צור טבלה:

בלוח המחוונים של DynamoDB, לחץ על "Create table".

Table name: הזן ShortUrls

Partition key: הזן id (ודא ש-"String" נבחר כסוג הנתונים).

Sort key: השאר ריק.

Table settings: השאר את הגדרות ברירת המחדל (או בחר "Customize settings" אם אתה רוצה לשנות).

Tags: אופציונלי, אך מומלץ להוסיף תגית כמו Project: URLShortener.

לחץ על "Create table".

(הערה: החלף את תמונת ה-Placeholder בצילום מסך אמיתי של יצירת הטבלה שלך.)

ודא שהטבלה נוצרה: הטבלה אמורה להופיע ברשימת הטבלאות שלך עם סטטוס "Active".

שלב 2: יצירת פונקציית AWS Lambda
פונקציית Lambda תטפל בלוגיקת הקיצור וההפניה של הכתובות.

עבור ל-Lambda: חפש "Lambda" בסרגל החיפוש ובחר בו.

צור פונקציה:

בלוח המחוונים של Lambda, לחץ על "Create function".

Author from scratch (בחר באפשרות זו).

Function name: הזן שם תיאורי, לדוגמה: URLShortenerLambda.

Runtime: בחר Python 3.9 (או גרסה עדכנית יותר זמינה).

Architecture: השאר ברירת מחדל (e.g., x86_64).

Permissions:

בחר "Use an existing role".

Existing role: בחר labrole מהרשימה הנפתחת (כפי שנדרש במשימה).

(הערה: החלף את תמונת ה-Placeholder בצילום מסך אמיתי של יצירת הפונקציה שלך.)

לחץ על "Create function".

הגדר את Function URL:

לאחר יצירת הפונקציה, נווט ללשונית "Configuration".

בצד שמאל, בחר "Function URL".

לחץ על "Create Function URL".

Auth type: בחר NONE (זה יאפשר גישה ציבורית ללא אימות).

CORS configuration: אופציונלי, אך מומלץ להוסיף:

Access-Control-Allow-Origin: * (כדי לאפשר ל-frontend גישה מכל דומיין).

Access-Control-Allow-Methods: GET, POST, OPTIONS.

Access-Control-Allow-Headers: Content-Type.

לחץ על "Save".

העתק את Function URL: לאחר השמירה, תראה את כתובת ה-URL שנוצרה. העתק אותה עכשיו! תצטרך אותה עבור קוד ה-frontend.

(הערה: החלף את תמונת ה-Placeholder בצילום מסך אמיתי של הגדרת ה-Function URL שלך.)

העלה את קוד ה-Lambda:

בלשונית "Code", תחת "Code source", לחץ על "Upload from" -> ".zip file".

ארז את הקובץ lambda_function.py לקובץ ZIP (לדוגמה, lambda_code.zip).

העלה את קובץ ה-ZIP שלך.

לחץ על "Deploy".

הגדר משתני סביבה:

בלשונית "Configuration", בחר "Environment variables".

לחץ על "Edit".

הוסף משתנה חדש:

Key: TABLE_NAME

Value: ShortUrls (זהו שם טבלת ה-DynamoDB שיצרת).

לחץ על "Save".

הגדר הרשאות (IAM Role):

פונקציית ה-Lambda שלך (עם התפקיד labrole) צריכה הרשאות כדי לגשת ל-DynamoDB.

נווט ל-IAM (Identity and Access Management) בקונסולת AWS.

בצד שמאל, בחר "Roles".

חפש את labrole ולחץ עליו.

בלשונית "Permissions", לחץ על "Add permissions" -> "Attach policies".

חפש ובחר את הפוליסי AmazonDynamoDBFullAccess (לצורך פשטות במעבדה, בדרך כלל תגדיר הרשאות ספציפיות יותר).

לחץ על "Attach policies".

(הערה: החלף את תמונת ה-Placeholder בצילום מסך אמיתי של הוספת ההרשאות.)

שלב 3: אירוח ה-Frontend ב-AWS S3
S3 ישמש לאירוח האתר הסטטי של מקצר הכתובות.

עבור ל-S3: חפש "S3" בסרגל החיפוש ובחר בו.

צור Bucket:

לחץ על "Create bucket".

Bucket name: הזן שם ייחודי גלובלית (לדוגמה: my-url-shortener-frontend-yourname-123).

AWS Region: בחר את אותו אזור כמו פונקציית ה-Lambda שלך.

Object Ownership: השאר ברירת מחדל (ACLs disabled).

Block Public Access settings for this bucket: בטל את הסימון ב-"Block all public access" (זה הכרחי לאירוח אתר סטטי).

אשר את האזהרה.

Bucket Versioning: השאר ברירת מחדל.

Tags: אופציונלי.

לחץ על "Create bucket".

(הערה: החלף את תמונת ה-Placeholder בצילום מסך אמיתי של יצירת ה-Bucket שלך.)

הפעל אירוח אתר סטטי:

לחץ על ה-Bucket שיצרת.

עבור ללשונית "Properties".

גלול מטה ל-"Static website hosting" ולחץ על "Edit".

בחר "Enable".

Index document: הזן index.html.

Error document: הזן index.html (או השאר ריק אם אין דף שגיאה מותאם אישית).

לחץ על "Save changes".

העתק את Endpoint ה-Bucket: תחת "Static website hosting", תראה את "Bucket website endpoint". העתק את ה-URL הזה! זהו ה-URL של האתר הסטטי שלך.

(הערה: החלף את תמונת ה-Placeholder בצילום מסך אמיתי של הגדרת אירוח האתר הסטטי שלך.)

העלה את קובץ index.html:

ודא שעדכנת את index.html עם ה-Lambda Function URL שהעתקת בשלב 2.

בלשונית "Objects" בתוך ה-Bucket שלך, לחץ על "Upload".

גרור ושחרר את הקובץ index.html שלך, או לחץ על "Add files".

לחץ על "Upload".

הגדר מדיניות Bucket (Bucket Policy):

בלשונית "Permissions" בתוך ה-Bucket שלך, גלול מטה ל-"Bucket policy".

לחץ על "Edit".

הדבק את מדיניות ה-Bucket הבאה, החלף את YOUR_BUCKET_NAME בשם ה-Bucket האמיתי שלך:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR_BUCKET_NAME/*"
            ]
        }
    ]
}

לחץ על "Save changes".

(הערה: החלף את תמונת ה-Placeholder בצילום מסך אמיתי של הגדרת ה-Bucket Policy שלך.)

שלב 4: אינטגרציה ובדיקה
הכל מוכן! כעת נבדוק את האפליקציה.

עדכון ה-Frontend (אם לא עשית זאת קודם):

פתח את קובץ index.html במחשב שלך.

מצא את השורה: const LAMBDA_FUNCTION_URL = 'YOUR_LAMBDA_FUNCTION_URL_HERE';

החלף את YOUR_LAMBDA_FUNCTION_URL_HERE בכתובת ה-URL של פונקציית ה-Lambda שהעתקת בשלב 2.

שמור את הקובץ.

העלה מחדש את index.html ל-S3: חזור ל-S3 Bucket שלך, העלה את הקובץ המעודכן, ואשר את ההחלפה.

בדיקת האפליקציה:

פתח דפדפן אינטרנט ונווט ל-Bucket website endpoint שהעתקת בשלב 3.

קיצור כתובת URL:

הזן כתובת URL ארוכה בשדה הקלט (לדוגמה: https://www.google.com/search?q=aws+url+shortener+tutorial).

לחץ על כפתור "קצר כתובת URL".

ודא שמופיע קישור מקוצר.

לחץ על כפתור "העתק" וודא שההודעה "הועתק בהצלחה!" מופיעה.

(הערה: החלף את תמונת ה-Placeholder בצילום מסך אמיתי של ה-frontend שלך מקצר כתובת.)

בדיקת הפניה מחדש:

העתק את הקישור המקוצר שנוצר.

פתח כרטיסייה חדשה בדפדפן והדבק את הקישור המקוצר בשורת הכתובות.

לחץ Enter.

ודא שאתה מופנה אוטומטית לכתובת ה-URL המקורית שהזנת.

(הערה: החלף את תמונת ה-Placeholder בצילום מסך אמיתי של ההפניה מחדש.)

בדיקת DynamoDB:

חזור לקונסולת DynamoDB.

בחר את טבלת ShortUrls.

עבור ללשונית "Explore items".

ודא שפריט חדש נוסף לטבלה עם ה-ID הקצר וה-URL המקורי.

שלב 5: העלאה ל-GitHub
צור מאגר GitHub חדש:

נווט ל-GitHub (https://github.com/).

התחבר ובחר "New repository".

תן שם למאגר (לדוגמה: aws-url-shortener).

בחר אם המאגר יהיה ציבורי או פרטי.

אופציונלי: הוסף קובץ README.md (תחליף אותו מאוחר יותר).

לחץ על "Create repository".

העלה את הקבצים שלך:

index.html: הקובץ הסטטי של ה-frontend.

lambda_function.py: קוד פונקציית ה-Lambda.

README.md: קובץ זה (המדריך המפורט שקראת כרגע).

אתה יכול להעלות את הקבצים ישירות דרך ממשק המשתמש של GitHub, או להשתמש ב-Git CLI:

# אתחל מאגר Git מקומי
git init

# הוסף את הקבצים שלך
git add index.html lambda_function.py README.md

# בצע קומיט לשינויים
git commit -m "Initial commit for AWS URL Shortener"

# הוסף את המאגר המרוחק (החלף ב-URL של המאגר שלך)
git remote add origin https://github.com/YOUR_USERNAME/aws-url-shortener.git

# דחוף את הקבצים למאגר GitHub
git push -u origin master

לאחר שתשמור את התוכן הזה בקובץ README.md בתיקייה שלך, תוכל להשתמש בו כמדריך מפורט לביצוע כל השלבים הנדרשים ב-AWS.