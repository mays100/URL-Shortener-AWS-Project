פרויקט מקצר כתובות URL ב-AWS
מבוא
פרויקט זה מציג יישום פשוט של מקצר כתובות URL (URL Shortener) המבוסס על שירותי Amazon Web Services (AWS) Serverless. הפרויקט מאפשר למשתמשים לקצר כתובות URL ארוכות ולקבל כתובות מקוצרות, אשר מפנות אוטומטית לכתובת המקורית בעת הגישה אליהן.

טכנולוגיות בשימוש:
AWS Lambda: פונקציה ללא שרתים (Serverless Function) המטפלת בלוגיקה העסקית של קיצור והפניית כתובות URL.

AWS DynamoDB: מסד נתונים NoSQL המשמש לאחסון הקישורים המקוריים והמקוצרים.

AWS S3: שירות אחסון אובייקטים המשמש לאירוח האתר הסטטי (Frontend) של מקצר הכתובות.

HTML, CSS (Tailwind CSS), JavaScript: עבור ממשק המשתמש (Frontend).

ארכיטקטורה
הארכיטקטורה של הפרויקט מורכבת משלושה חלקים עיקריים:

Frontend (ממשק משתמש):

קובץ index.html סטטי המאוחסן ב-AWS S3.

מכיל טופס HTML לקליטת כתובת URL ארוכה וכפתור לקיצור.

משתמש ב-JavaScript כדי לשלוח בקשות POST לפונקציית ה-Lambda לקיצור כתובות, ומטפל בהצגת הקישור המקוצר.

Backend (לוגיקה עסקית):

פונקציית AWS Lambda (URLShortenerLambda) כתובה בפייתון.

מקבלת בקשות POST מה-Frontend לקיצור URL, מייצרת short_id ייחודי, ושומרת את הקישור המקורי והמקוצר ב-DynamoDB.

מקבלת בקשות GET ל-short_id (כאשר משתמש ניגש לקישור מקוצר), מאחזרת את ה-URL המקורי מ-DynamoDB, ומבצעת הפניה (Redirect) לדפדפן.

מוגדרת עם Function URL ועם הגדרות CORS מתאימות כדי לאפשר גישה מה-Frontend.

Database (מסד נתונים):

טבלת AWS DynamoDB (ShortUrls).

מפתח מחיצה (Partition Key) בשם short_id (מסוג String) המשמש כמזהה ייחודי לכל קישור מקוצר.

הוראות הגדרה והפעלה
כדי להגדיר ולהפעיל את הפרויקט, יש לבצע את השלבים הבאים בסדר הנתון:

יצירת טבלת DynamoDB:

ב-AWS Console, נווטו ל-DynamoDB.

צרו טבלה חדשה בשם ShortUrls.

הגדירו את short_id כמפתח מחיצה (Partition Key) מסוג String.

יצירת פונקציית AWS Lambda:

ב-AWS Console, נווטו ל-Lambda.

צרו פונקציה חדשה:

Function name: URLShortenerLambda

Runtime: Python 3.13 (או גרסה עדכנית יותר).

Execution role: בחרו LabRole (או תפקיד עם הרשאות מתאימות ל-DynamoDB).

הדביקו את קוד הפייתון המלא שסופק לתוך עורך הקוד של הפונקציה ולחצו "Deploy".

הגדרת Function URL:

בלשונית Configuration -> Function URL, צרו Function URL חדש.

Auth type: NONE.

CORS configuration:

Allow origins: *

Allow headers: Content-Type, X-Amz-Date, Authorization

Allow methods: POST, GET

העתיקו את ה-Function URL שנוצר.

הגדרת Environment variable:

בלשונית Configuration -> Environment variables, לחצו "Edit".

הוסיפו משתנה סביבה: Key: TABLE_NAME, Value: ShortUrls.

אירוח ה-Frontend ב-AWS S3:

ב-AWS Console, נווטו ל-S3.

צרו Bucket חדש:

Bucket name: שם ייחודי וגלובלי (לדוגמה: my-url-shortener-frontend-mayasabag321-2025).

Block Public Access settings: בטלו את הסימון מ"Block all public access" ואשרו את ההודעה.

הפעלת Static website hosting:

בלשונית Properties של ה-Bucket, גללו ל-"Static website hosting" ולחצו "Edit".

סמנו Enable.

Index document: index.html.

Error document: index.html (או השאר ריק אם אין דף שגיאה מותאם אישית).

העתיקו את ה-"Bucket website endpoint" שנוצר.

עדכון קובץ index.html:

פתחו את קובץ index.html המקומי שלכם.

מצאו את השורה: const LAMBDA_FUNCTION_URL = '...'

החליפו את ה-URL בתוך הגרשיים ב-Function URL המדויק שהעתקתם משלב 2.

שמרו את הקובץ.

העלאת קובץ index.html ל-S3:

בלשונית Objects של ה-Bucket, לחצו "Upload".

העלו את קובץ index.html המעודכן.

הגדרת Bucket Policy:

בלשונית Permissions של ה-Bucket, גללו ל-"Bucket policy" ולחצו "Edit".

הדביקו את המדיניות הבאה (וודאו ששם ה-Bucket תואם לשלכם):

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
                "arn:aws:s3:::my-url-shortener-frontend-mayasabag321-2025/*"
            ]
        }
    ]
}

לחצו "Save changes".

בדיקת הפרויקט
גישה לאתר: פתחו את ה-"Bucket website endpoint" (כתובת האתר הסטטי ב-S3) בדפדפן. האתר אמור להיטען.

קיצור כתובת URL: הזינו כתובת URL ארוכה (לדוגמה: https://www.amazon.com/Echo-Dot-3rd-Gen-Charcoal/dp/B07FZ8S7FG/ref=sr_1_1?qid=1678886400&refinements=p_89%3AAmazon&rnid=2528832011&s=electronics&sr=8-1) ולחצו "קצר כתובת URL". קישור מקוצר אמור להופיע.

בדיקת הפניה מחדש: העתיקו את הקישור המקוצר, הדביקו אותו בכרטיסייה חדשה בדפדפן, ולחצו Enter. אתם אמורים להיות מופנים לכתובת ה-URL המקורית.

אימות ב-DynamoDB: ב-AWS Console, נווטו ל-DynamoDB -> Tables -> ShortUrls -> Explore items. ודאו שהקישור החדש נוסף לטבלה.

צילומי מסך
תיקיית screenshots בפרויקט זה מכילה את צילומי המסך המתעדים את שלבי ההגדרות והבדיקות השונים ב-AWS Console ובדפדפן. צילומי המסך מסודרים לפי שלבי ההקמה והבדיקה.