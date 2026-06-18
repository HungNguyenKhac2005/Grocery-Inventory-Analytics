# 🧠 Teen Mental Health & Social Media Analysis

## ✒️ 1. Giới thiệu về tác giả

- **Tên:** Nguyễn Khắc Hưng
- **Vị trí:** Data Analyst
- **Học vấn:** Đang theo học chương trình kỹ sư ngành Khoa học Dữ liệu, chuyên ngành Phân tích Dữ liệu trong Kinh tế và Tài chính, thuộc Khoa Công nghệ Thông tin, Trường Đại học Mỏ - Địa chất.

---

## 📌 Đặt vấn đề (Problem Statements)

Dưới đây là 9 câu hỏi/vấn đề thực tế (business questions) cần khai phá từ bộ dữ liệu:

- **Vấn đề 1 (Phân mảnh hành vi cốt lõi):** Thời lượng sử dụng mạng xã hội trung bình (`daily_social_media_hours`) và mức độ nghiện (`addiction_level`) có sự phân hóa như thế nào giữa các nhóm giới tính (`gender`) và các độ tuổi (`age`) khác nhau?
- **Vấn đề 2 (Đặc thù nền tảng):** Nhóm người dùng chỉ dùng TikTok, chỉ dùng Instagram, và dùng cả hai (`platform_usage`) có sự chênh lệch ra sao về kết quả học tập (`academic_performance`) và mức độ căng thẳng (`anxiety_level`)?
- **Vấn đề 3 (Phân tích tương quan & Chẩn đoán):** Có mối tương quan nghịch biến rõ rệt nào giữa thời gian dùng điện thoại trước khi ngủ (`screen_time_before_sleep`) và tổng số giờ ngủ (`sleep_hours`) không?
- **Vấn đề 4 (Nghịch lý giao tiếp xã hội):** Những cá nhân có mức độ tương tác xã hội đời thực thấp (`social_interaction_level = low`) liệu có xu hướng bù đắp bằng cách tiêu tốn nhiều `daily_social_media_hours` hơn các nhóm 'medium' và 'high' không?
- **Vấn đề 5 (Tác động kép đến sức khỏe tâm thần):** Trong 3 biến: việc thiếu ngủ (`sleep_hours`), thời lượng dùng MXH (`daily_social_media_hours`), và mức độ nghiện (`addiction_level`), yếu tố nào đẩy mức độ lo âu (`anxiety_level`) lên cao nhất?
- **Vấn đề 6 (Vai trò của thể chất):** Hoạt động thể chất (`physical_activity`) có đóng vai trò như một "tấm khiên" bảo vệ sức khỏe tinh thần không? Hãy so sánh mức căng thẳng của nhóm có vận động thể chất cao với nhóm thấp, trong điều kiện cả hai nhóm có cùng thời lượng dùng MXH.
- **Vấn đề 7 (Chân dung nhóm rủi ro cao - High-Risk Persona):** Hãy dùng SQL (kết hợp CTE và CASE WHEN) để lọc ra nhóm người dùng có dấu hiệu đáng báo động (ví dụ quy ước: `sleep_hours < 5`, `anxiety_level > 7`, `stress_level > 7`). Nhóm này có chung đặc điểm gì về nền tảng sử dụng và thói quen trước khi ngủ?
- **Vấn đề 8 (Tìm kiếm ngưỡng an toàn - Tipping Point):** Từ dữ liệu điểm học tập (`academic_performance`), hãy gom nhóm và tìm ra "điểm gãy" – tức là vượt qua mốc bao nhiêu giờ `daily_social_media_hours` thì điểm học tập bắt đầu lao dốc một cách rõ rệt nhất?
- **Vấn đề 9 (Phân tích nhãn Trầm cảm - depression_label):** Đâu là những đặc điểm nhận diện rõ ràng nhất của nhóm được gắn nhãn trầm cảm (`depression_label = 1`) so với nhóm bằng 0? Nhóm này có dùng MXH nhiều hơn mức bình thường không?

---

## 🛠️ Công cụ sử dụng (Tools)

- **PostgreSQL**: Hệ quản trị cơ sở dữ liệu quan hệ mạnh mẽ, được sử dụng để lưu trữ và truy vấn dữ liệu.
- **SQL**: Ngôn ngữ truy vấn cấu trúc dùng để tạo bảng, truy vấn, tổng hợp và phân tích dữ liệu để tìm insight.
- **DBeaver**: IDE trực quan để viết truy vấn SQL và quản lý cơ sở dữ liệu.

---

## 📊 Phân tích chi tiết (Data Analysis & Insights)

Mỗi truy vấn dưới đây được thiết kế nhằm giải quyết các câu hỏi phân tích cụ thể, tìm ra các phát hiện giá trị từ dữ liệu.

### **Vấn đề 1**: Phân tích mức độ phân hóa của `daily_social_media_hours` và `addiction_level` theo giới tính và nhóm độ tuổi

```sql
-- Tạo View phân tích thời lượng sử dụng MXH và mức độ nghiện theo giới tính và nhóm tuổi
CREATE VIEW social_media_addiction_by_gender_age_group AS
WITH age_group_table AS (
    SELECT 
        gender,
        daily_social_media_hours,
        addiction_level,
        CASE
            WHEN age >= 13 AND age < 15 THEN '13-15'
            WHEN age >= 15 AND age < 18 THEN '15-18'
            WHEN age >= 18 THEN '18+'
        END AS age_group
    FROM teen_mental_health_analysis
)
SELECT 
    gender,
    age_group,
    ROUND(AVG(daily_social_media_hours)::numeric, 2) AS avg_daily_social_media_hours,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY daily_social_media_hours) AS median_daily_social_media_hours,
    ROUND(AVG(addiction_level)::numeric, 2) AS avg_addiction_level,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY addiction_level) AS median_addiction_level
FROM age_group_table
GROUP BY 
    gender,
    age_group;

-- Xem kết quả từ View
SELECT * FROM social_media_addiction_by_gender_age_group;
```

#### **Kết quả truy vấn (Output)**

| Gender | Age Group | Avg Daily Social Media Hours | Median Daily Social Media Hours | Avg Addiction Level | Median Addiction Level |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Female | 13-15 | 4.31 | 4.10 | 5.54 | 6.00 |
| Female | 15-18 | 4.67 | 4.80 | 5.36 | 6.00 |
| Female | 18+ | 4.47 | 4.30 | 5.64 | 6.00 |
| Male | 13-15 | 4.56 | 4.60 | 5.48 | 6.00 |
| Male | 15-18 | 4.75 | 4.75 | 5.62 | 6.00 |
| Male | 18+ | 4.30 | 4.50 | 5.83 | 6.00 |

#### **Nhận xét & Insight (Insights)**

- Đối với thời gian sử dụng điện thoại trung bình thì nhóm nữ giới từ 13-15 và 15-18 tuổi sử dụng ít hơn so với nhóm nam giới cùng độ tuổi, nhóm từ trên 18 tuổi thì nữ lại có xu hướng dùng nhiều hơn. Đối với mức độ nghiện thì hai nhóm 15-18 tuổi và trên 18 tuổi ở nam giới có xu hướng nghiện nặng hơn so với nhóm nữ giới cùng tuổi, riêng nhóm nữ giới 13-15 tuổi thì lại có mức độ nghiện cao hơn nhóm nam giới cùng tuổi.
- Nhóm sử dụng điện thoại trung bình một ngày nhiều nhất là nhóm nam giới từ 15-18 tuổi. Nhóm sử dụng trung bình một ngày thấp nhất là nhóm nam giới trên 18 tuổi và nữ giới từ 13-15 tuổi.
- Nhóm có mức độ nghiện cao nhất là nam giới trên 18 tuổi và nhóm có mức độ nghiện thấp nhất là nữ giới từ 13-15 tuổi.
- Nhìn chung, đối với nhóm giới tính thì nam giới có xu hướng sử dụng điện thoại nhiều hơn và mức độ nghiện cũng cao hơn nữ giới. Đối với nhóm độ tuổi, người trên 18 tuổi có xu hướng sử dụng điện thoại ít hơn người dưới 18 tuổi.
- Trong ba nhóm độ tuổi, nhóm từ 13-15 tuổi có thời lượng sử dụng nhiều nhất. Tuy nhiên ở mức độ nghiện, người trên 18 tuổi có thời lượng sử dụng ít nhưng lại có mức độ nghiện cao hơn khá nhiều so với hai nhóm còn lại.

---

### **Vấn đề 2**: Phân tích mức độ ảnh hưởng của các loại mạng xã hội đến kết quả học tập và chỉ số lo âu

```sql
-- Tạo View phân tích kết quả học tập và lo âu theo nền tảng sử dụng
CREATE VIEW academic_anxiety_summary_by_platform_usage AS
SELECT
    platform_usage,
    COUNT(*) AS total,
    ROUND(AVG(academic_performance)::numeric, 2) AS avg_academic_performance,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY academic_performance) AS median_academic_performance,
    ROUND(AVG(anxiety_level)::numeric, 2) AS avg_anxiety_level,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY anxiety_level) AS median_anxiety_level
FROM teen_mental_health_analysis
GROUP BY platform_usage;

-- Xem kết quả từ View
SELECT * FROM academic_anxiety_summary_by_platform_usage;
```

#### **Kết quả truy vấn (Output)**

| Platform Usage | Total | Avg Academic Performance | Median Academic Performance | Avg Anxiety Level | Median Anxiety Level |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Both | 391 | 2.98 | 2.99 | 5.49 | 5.0 |
| Instagram | 411 | 3.00 | 3.00 | 5.67 | 6.0 |
| TikTok | 398 | 3.00 | 2.97 | 5.75 | 6.0 |

#### **Nhận xét & Insight (Insights)**

- Quan sát ta thấy nhóm sử dụng cả hai loại mạng xã hội là Instagram và TikTok thì có điểm tổng kết học tập trung bình thấp hơn nhóm người chỉ sử dụng hoặc Instagram hoặc TikTok.
- Đối với chỉ số lo âu, nhóm người sử dụng cả hai loại mạng xã hội (Both) lại có chỉ số lo âu trung bình thấp hơn so với nhóm người chỉ sử dụng TikTok hoặc Instagram.

---

### **Vấn đề 3**: Phân tích mối tương quan giữa thời gian sử dụng điện thoại trước khi ngủ và thời gian ngủ

```sql
-- Tính hệ số tương quan giữa thời gian sử dụng điện thoại trước khi ngủ và số giờ ngủ
SELECT
    CORR(screen_time_before_sleep, sleep_hours) AS correlation
FROM teen_mental_health_analysis;
```

#### **Kết quả truy vấn (Output)**

| Correlation |
| :---: |
| 0.0102352814 |

#### **Nhận xét & Insight (Insights)**

- Quan sát ta thấy không có mối tương quan nghịch biến rõ rệt nào giữa thời gian sử dụng điện thoại trước khi ngủ và thời gian ngủ. Độ tương quan rất thấp (~0.01) cho thấy thời gian ngủ không bị ảnh hưởng trực tiếp bởi thời gian sử dụng điện thoại trước khi ngủ trong bộ dữ liệu này.

---

### **Vấn đề 4**: Phân tích mức độ tương quan giữa thời gian sử dụng mạng xã hội và mức độ tương tác xã hội

```sql
-- Tạo View phân tích thời lượng sử dụng MXH theo mức độ tương tác xã hội ngoài đời thực
CREATE VIEW social_media_usage_summary_by_social_interaction_level AS
SELECT
    social_interaction_level,
    COUNT(*) AS total,
    SUM(daily_social_media_hours) AS total_daily_social_media_hours,
    ROUND(AVG(daily_social_media_hours)::numeric, 2) AS avg_daily_social_media_hours,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY daily_social_media_hours) AS median_daily_social_media_hours
FROM teen_mental_health_analysis
GROUP BY social_interaction_level;

-- Xem kết quả từ View
SELECT * FROM social_media_usage_summary_by_social_interaction_level;
```

#### **Kết quả truy vấn (Output)**

| Social Interaction Level | Total | Total Daily Social Media Hours | Avg Daily Social Media Hours | Median Daily Social Media Hours |
| :--- | :---: | :---: | :---: | :---: |
| High | 369 | 1644.7 | 4.46 | 4.3 |
| Low | 415 | 1883.9 | 4.54 | 4.6 |
| Medium | 416 | 1915.4 | 4.60 | 4.6 |

#### **Nhận xét & Insight (Insights)**

- Nhóm sử dụng mạng xã hội nhiều nhất là nhóm Medium. Điều này cho thấy những người có mức độ tương tác xã hội ngoài đời ở mức trung bình lại dành thời gian nhiều nhất cho mạng xã hội.
- Nhóm sử dụng mạng xã hội ít nhất là nhóm High. Điều này khá hợp lý vì những người có mức độ tương tác xã hội cao thường thích tham gia các hoạt động bên ngoài (thể thao, gặp gỡ trò chuyện trực tiếp) thay vì dùng mạng xã hội.
- Đối với nhóm có mức độ tương tác xã hội thấp (Low) thì thời lượng sử dụng mạng xã hội hàng ngày cũng ở mức khá cao (trung bình 4.54 giờ/ngày).
- Nhìn tổng quát, mức độ tương tác xã hội có ảnh hưởng đến thời gian sử dụng mạng xã hội theo xu hướng bù đắp, tuy nhiên mức độ ảnh hưởng và chênh lệch là tương đối thấp.

---

### **Vấn đề 5**: Trong 3 biến việc thiếu ngủ (`sleep_hours`), thời lượng dùng MXH (`daily_social_media_hours`), và mức độ nghiện (`addiction_level`), yếu tố nào đẩy mức độ lo âu (`anxiety_level`) lên cao nhất?

```sql
-- Tính hệ số tương quan giữa mức độ lo âu (anxiety_level) với 3 yếu tố: giấc ngủ, thời lượng MXH, và độ nghiện
SELECT
    CORR(sleep_hours, anxiety_level) AS corr_anxiety_level_sleep_hours,
    CORR(daily_social_media_hours, anxiety_level) AS corr_anxiety_level_daily_social_media_hours,
    CORR(addiction_level, anxiety_level) AS corr_anxiety_level_addiction_level
FROM teen_mental_health_analysis;
```

#### **Kết quả truy vấn (Output)**

| Corr: Anxiety Level vs Sleep Hours | Corr: Anxiety Level vs Daily Social Media Hours | Corr: Anxiety Level vs Addiction Level |
| :---: | :---: | :---: |
| -0.0118786929 | 0.0278347563 | 0.0311537836 |

#### **Nhận xét & Insight (Insights)**

- Quan sát từ bảng số liệu ta thấy hệ số tương quan của cả 3 biến với chỉ số lo âu đều rất thấp (gần như bằng 0, không có mối liên kết tuyến tính rõ rệt).
- Trong 3 yếu tố kể trên, mức độ nghiện mạng xã hội (`addiction_level`) có tương quan đồng biến cao nhất (`0.031`), tiếp theo là thời gian dùng mạng xã hội hàng ngày (`0.028`). Việc thiếu ngủ (`sleep_hours`) có hệ số tương quan âm rất nhỏ (`-0.011`).
- Nhìn chung, dù mức độ nghiện là yếu tố có tương quan lớn nhất nhưng chỉ số này vẫn quá thấp. Điều này cho thấy cả 3 biến đều không quyết định trực tiếp chỉ số lo âu của các bạn trẻ, và lo âu có thể do nhiều tác nhân tâm lý hoặc đời sống khác ngoài các biến này gây ra.

---

### **Vấn đề 6**: Vai trò của thể chất: Hoạt động thể chất (`physical_activity`) có đóng vai trò như một "tấm khiên" bảo vệ sức khỏe tinh thần không?

Hãy so sánh mức căng thẳng của nhóm có vận động thể chất cao với nhóm thấp, trong điều kiện cả hai nhóm có cùng thời lượng dùng MXH.

```sql
-- Tạo View phân tích mức độ căng thẳng theo nhóm thời gian sử dụng MXH và nhóm hoạt động thể chất
CREATE VIEW stress_analysis_by_behavior_groups AS
WITH activity_social_groups AS (
    SELECT 
        physical_activity, 
        daily_social_media_hours,
        stress_level,
        CASE
            WHEN daily_social_media_hours < 2.8 THEN 'Dùng ít'
            WHEN daily_social_media_hours >= 2.8 AND daily_social_media_hours <= 6.3 THEN 'Dùng trung bình'
            WHEN daily_social_media_hours > 6.3 THEN 'Dùng nhiều'
        END AS social_media_hours_group,
        CASE
            WHEN physical_activity < 0.5 THEN 'Tập ít'
            WHEN physical_activity >= 0.5 AND physical_activity <= 1.5 THEN 'Tập trung bình'
            WHEN physical_activity > 1.5 THEN 'Tập nhiều'
        END AS physical_activity_group
    FROM teen_mental_health_analysis
)
SELECT 
    social_media_hours_group, 
    physical_activity_group,
    COUNT(*) AS total,
    ROUND(AVG(stress_level)::numeric, 2) AS avg_stress_level,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY stress_level) AS median_stress_level
FROM activity_social_groups
GROUP BY 
    social_media_hours_group, 
    physical_activity_group;

-- Xem kết quả từ View
SELECT * FROM stress_analysis_by_behavior_groups;
```

#### **Kết quả truy vấn (Output)**

| Social Media Hours Group | Physical Activity Group | Total | Avg Stress Level | Median Stress Level |
| :--- | :--- | :---: | :---: | :---: |
| Dùng ít | Tập ít | 69 | 5.65 | 6.0 |
| Dùng ít | Tập trung bình | 153 | 5.51 | 5.0 |
| Dùng ít | Tập nhiều | 77 | 5.26 | 5.0 |
| Dùng trung bình | Tập ít | 138 | 5.00 | 5.0 |
| Dùng trung bình | Tập trung bình | 329 | 5.39 | 5.0 |
| Dùng trung bình | Tập nhiều | 136 | 5.27 | 5.0 |
| Dùng nhiều | Tập ít | 62 | 5.47 | 5.5 |
| Dùng nhiều | Tập trung bình | 168 | 5.96 | 6.0 |
| Dùng nhiều | Tập nhiều | 68 | 5.53 | 5.0 |

#### **Nhận xét & Insight (Insights)**

- Ở nhóm dùng ít mạng xã hội, ta thấy rõ ràng hoạt động thể chất đóng vai trò như một tấm khiên bảo vệ khi chỉ số stress trung bình giảm dần từ 5.65 (tập ít) xuống 5.51 (tập trung bình) và thấp nhất là 5.26 (tập nhiều).
- Tuy nhiên, ở hai nhóm dùng trung bình và dùng nhiều mạng xã hội, xu hướng này không còn đồng đều nữa. Nhóm dùng nhiều MXH có mức stress khá cao ở những người tập trung bình (5.96) so với tập ít (5.47) và tập nhiều (5.53).
- Kết luận lại thì hoạt động thể chất giúp giảm stress tốt nhất khi người dùng kiểm soát được thời gian lướt mạng xã hội ở mức thấp. Nếu thời lượng dùng MXH quá nhiều thì vận động thể chất không còn duy trì được vai trò bảo vệ tinh thần một cách rõ rệt.

---

### **Vấn đề 7**: Chân dung nhóm rủi ro cao (High-Risk Persona)

Hãy dùng SQL để lọc ra nhóm người dùng có dấu hiệu đáng báo động (Ví dụ quy ước: `sleep_hours < 5`, `anxiety_level > 7`, `stress_level > 7`). Nhóm này có chung đặc điểm gì về nền tảng sử dụng và thói quen trước khi ngủ?

```sql
-- Lọc danh sách nhóm người dùng có rủi ro cao
SELECT * 
FROM teen_mental_health_analysis
WHERE sleep_hours < 5 
  AND anxiety_level > 7 
  AND stress_level > 7;
```

#### **Kết quả truy vấn (Output)**

| Age | Gender | Daily Social Media Hours | Platform Usage | Sleep Hours | Screen Time Before Sleep | Academic Performance | Physical Activity | Social Interaction Level | Stress Level | Anxiety Level | Addiction Level | Depression Label |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| 19 | male | 1.3 | Instagram | 4.5 | 0.7 | 2.51 | 0.8 | low | 10 | 9 | 7 | 0 |
| 14 | female | 4.4 | Both | 4.2 | 2.6 | 2.28 | 1.3 | medium | 8 | 10 | 4 | 0 |
| 15 | male | 3.6 | TikTok | 4.3 | 2.9 | 2.20 | 1.0 | high | 10 | 9 | 7 | 0 |
| 19 | male | 4.4 | TikTok | 4.3 | 0.8 | 2.44 | 1.0 | high | 9 | 9 | 7 | 0 |
| 13 | male | 7.5 | TikTok | 4.8 | 0.7 | 2.91 | 2.0 | high | 10 | 9 | 1 | 1 |
| 17 | male | 4.0 | Both | 4.3 | 1.8 | 2.17 | 0.9 | high | 8 | 8 | 3 | 0 |
| 14 | male | 1.4 | Both | 4.5 | 1.4 | 3.17 | 1.7 | high | 9 | 10 | 9 | 0 |
| 13 | female | 7.2 | Both | 4.2 | 2.5 | 2.65 | 1.6 | low | 10 | 9 | 3 | 1 |
| 19 | male | 5.2 | Instagram | 4.3 | 1.3 | 2.29 | 1.3 | medium | 10 | 8 | 10 | 1 |
| 19 | male | 7.7 | Instagram | 4.2 | 2.6 | 2.20 | 1.8 | low | 8 | 9 | 4 | 1 |
| 19 | male | 7.0 | TikTok | 4.5 | 2.3 | 3.26 | 1.7 | high | 9 | 10 | 3 | 1 |
| 14 | female | 5.3 | Both | 4.7 | 1.1 | 3.68 | 1.8 | high | 10 | 8 | 10 | 1 |
| 13 | male | 2.1 | Instagram | 4.1 | 1.6 | 2.12 | 1.8 | high | 10 | 9 | 6 | 0 |
| 14 | male | 6.2 | TikTok | 4.4 | 0.7 | 3.45 | 0.5 | medium | 9 | 10 | 3 | 1 |
| 19 | female | 1.2 | TikTok | 4.8 | 1.7 | 2.16 | 0.6 | medium | 10 | 10 | 10 | 0 |
| 18 | female | 6.4 | Both | 4.2 | 1.1 | 2.68 | 0.3 | high | 10 | 9 | 4 | 1 |
| 19 | male | 4.6 | Both | 4.6 | 2.5 | 2.40 | 1.0 | high | 10 | 10 | 8 | 0 |
| 15 | female | 7.3 | Instagram | 4.1 | 2.1 | 2.87 | 0.4 | low | 10 | 10 | 1 | 1 |
| 15 | female | 7.8 | Instagram | 4.6 | 3.0 | 2.44 | 1.4 | medium | 8 | 10 | 6 | 1 |
| 18 | female | 2.2 | Instagram | 4.4 | 1.7 | 2.86 | 1.1 | high | 8 | 9 | 7 | 0 |
| 17 | male | 6.9 | Both | 4.6 | 2.5 | 2.04 | 0.8 | high | 10 | 9 | 2 | 1 |
| 18 | female | 6.3 | TikTok | 4.8 | 1.2 | 2.91 | 1.3 | medium | 9 | 10 | 3 | 1 |
| 14 | female | 1.6 | TikTok | 4.8 | 2.4 | 2.97 | 1.9 | low | 9 | 9 | 10 | 0 |
| 19 | male | 8.0 | TikTok | 4.7 | 0.5 | 2.18 | 0.6 | medium | 8 | 8 | 6 | 1 |

#### **Nhận xét & Insight (Insights)**

- Nhóm người dùng có rủi ro cao (24 học sinh lọc ra) sở hữu tỷ lệ trầm cảm đáng báo động khi có tới 11 người đã được gắn nhãn trầm cảm (`depression_label = 1`), chiếm gần một nửa nhóm.
- Về nền tảng sử dụng, nhóm này có xu hướng sử dụng TikTok hoặc cả hai mạng xã hội (Both) chiếm số lượng áp đảo với 18/24 người, trong khi chỉ dùng Instagram có số lượng ít hơn.
- Về thói quen trước khi ngủ, đa phần học sinh trong nhóm này sử dụng điện thoại trước khi ngủ rất nhiều (phổ biến từ 1.5 đến 3 giờ). Điều này kết hợp với thời lượng ngủ cực ít (dưới 5 tiếng) cho thấy mối liên kết rõ ràng giữa thói quen dùng màn hình muộn gây mất ngủ và ảnh hưởng xấu đến tâm lý của họ.

---

### **Vấn đề 8**: Tìm kiếm ngưỡng an toàn (Tipping Point)

Từ dữ liệu điểm học tập (`academic_performance`), hãy gom nhóm và tìm ra "điểm gãy" – tức là vượt qua mốc bao nhiêu giờ `daily_social_media_hours` thì điểm học tập bắt đầu lao dốc một cách rõ rệt nhất?

```sql
-- Phân tích tìm kiếm ngưỡng an toàn của thời lượng dùng MXH đối với kết quả học tập
WITH hourly_stats AS (
    SELECT 
        FLOOR(daily_social_media_hours) AS hour_daily,
        COUNT(*) AS total_student,
        ROUND(AVG(academic_performance)::numeric, 2) AS avg_academic_performance,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY academic_performance) AS median_academic_performance
    FROM teen_mental_health_analysis
    GROUP BY FLOOR(daily_social_media_hours)
)
SELECT
    hour_daily::numeric || '-' || (hour_daily::numeric + 1) || ' hour' AS usage_duration,
    total_student,
    avg_academic_performance,
    avg_academic_performance - LAG(avg_academic_performance) OVER (ORDER BY hour_daily::numeric DESC) AS performance_drop
FROM hourly_stats
ORDER BY hour_daily DESC;
```

#### **Kết quả truy vấn (Output)**

| Usage Duration | Total Student | Avg Academic Performance | Performance Drop |
| :--- | :---: | :---: | :---: |
| 8-9 hour | 14 | 2.93 | *None* |
| 7-8 hour | 191 | 3.06 | 0.13 |
| 6-7 hour | 146 | 2.97 | -0.09 |
| 5-6 hour | 181 | 3.00 | 0.03 |
| 4-5 hour | 166 | 2.91 | -0.09 |
| 3-4 hour | 171 | 2.97 | 0.06 |
| 2-3 hour | 180 | 2.99 | 0.02 |
| 1-2 hour | 151 | 3.02 | 0.03 |

#### **Nhận xét & Insight (Insights)**

- Điểm học tập trung bình của học sinh ở các nhóm thời gian sử dụng mạng xã hội nhìn chung dao động khá ổn định từ 2.91 đến 3.06, chưa thấy có sự sụt giảm nghiêm trọng hay đột ngột nào.
- Nhóm sử dụng nhiều nhất là 8-9 tiếng có điểm học tập thấp thứ hai (2.93), tuy nhiên nhóm dùng 7-8 tiếng lại đạt điểm trung bình cao nhất (3.06). Nhóm có điểm thấp nhất rơi vào mốc 4-5 tiếng (2.91).
- Tóm lại, trong tập dữ liệu này chưa xuất hiện một "điểm gãy" (tipping point) rõ rệt nào mà tại đó kết quả học tập bị ảnh hưởng tiêu cực có hệ thống theo thời gian sử dụng mạng xã hội tăng lên.

---

### **Vấn đề 9**: Phân tích nhãn Trầm cảm (`depression_label`)

Đâu là những đặc điểm nhận diện rõ ràng nhất của nhóm được gắn nhãn trầm cảm (`depression_label = 1`) so với nhóm bằng 0? Nhóm này có dùng MXH nhiều hơn mức bình thường không?

```sql
-- Phân tích những đặc điểm của nhóm người dùng được chẩn đoán bị trầm cảm
SELECT * 
FROM teen_mental_health_analysis
WHERE depression_label = 1;
```

#### **Kết quả truy vấn (Output)**

*Tổng số học sinh ghi nhận trầm cảm (`depression_label = 1`):* **31** học sinh.

| Age | Gender | Daily Social Media Hours | Platform Usage | Sleep Hours | Screen Time Before Sleep | Academic Performance | Physical Activity | Social Interaction Level | Stress Level | Anxiety Level | Addiction Level | Depression Label |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| 18 | male | 6.2 | Instagram | 4.1 | 2.8 | 3.41 | 1.1 | medium | 7 | 8 | 1 | 1 |
| 15 | female | 7.8 | TikTok | 5.3 | 0.5 | 2.32 | 0.8 | low | 8 | 9 | 3 | 1 |
| 13 | male | 7.8 | Instagram | 5.0 | 1.8 | 3.57 | 1.5 | medium | 8 | 10 | 3 | 1 |
| 15 | male | 5.1 | Instagram | 4.1 | 2.8 | 3.79 | 0.8 | medium | 9 | 7 | 3 | 1 |
| 13 | male | 7.5 | TikTok | 4.8 | 0.7 | 2.91 | 2.0 | high | 10 | 9 | 1 | 1 |
| 13 | female | 7.2 | Both | 4.2 | 2.5 | 2.65 | 1.6 | low | 10 | 9 | 3 | 1 |
| 19 | male | 5.2 | Instagram | 4.3 | 1.3 | 2.29 | 1.3 | medium | 10 | 8 | 10 | 1 |
| 15 | female | 5.2 | TikTok | 5.6 | 1.5 | 3.13 | 0.1 | low | 7 | 9 | 4 | 1 |
| 19 | male | 7.7 | Instagram | 4.2 | 2.6 | 2.20 | 1.8 | low | 8 | 9 | 4 | 1 |
| 16 | female | 7.4 | TikTok | 5.5 | 1.8 | 2.13 | 0.3 | high | 7 | 9 | 9 | 1 |
| 19 | male | 7.0 | TikTok | 4.5 | 2.3 | 3.26 | 1.7 | high | 9 | 10 | 3 | 1 |
| 19 | male | 6.0 | Instagram | 4.2 | 0.9 | 2.41 | 0.8 | medium | 7 | 9 | 9 | 1 |
| 16 | female | 5.3 | Both | 5.6 | 2.5 | 2.73 | 1.3 | medium | 7 | 10 | 4 | 1 |
| 14 | female | 5.3 | Both | 4.7 | 1.1 | 3.68 | 1.8 | high | 10 | 8 | 10 | 1 |
| 15 | female | 8.0 | Both | 5.7 | 1.3 | 3.54 | 0.1 | high | 9 | 7 | 5 | 1 |
| 18 | female | 7.2 | TikTok | 5.0 | 1.4 | 3.65 | 1.1 | low | 8 | 8 | 4 | 1 |
| 14 | male | 6.2 | TikTok | 4.4 | 0.7 | 3.45 | 0.5 | medium | 9 | 10 | 3 | 1 |
| 17 | female | 7.5 | TikTok | 5.4 | 2.3 | 3.44 | 0.4 | medium | 7 | 9 | 7 | 1 |
| 13 | male | 7.7 | Instagram | 4.4 | 2.0 | 3.09 | 1.0 | high | 8 | 7 | 8 | 1 |
| 16 | female | 5.3 | TikTok | 4.3 | 1.5 | 2.54 | 0.3 | high | 7 | 7 | 10 | 1 |
| 16 | female | 6.9 | Instagram | 5.8 | 0.6 | 3.65 | 0.5 | high | 10 | 8 | 10 | 1 |
| 18 | female | 6.4 | Both | 4.2 | 1.1 | 2.68 | 0.3 | high | 10 | 9 | 4 | 1 |
| 15 | male | 5.4 | TikTok | 5.2 | 0.6 | 3.65 | 1.5 | low | 7 | 9 | 10 | 1 |
| 15 | male | 7.8 | Both | 4.2 | 2.1 | 3.42 | 0.0 | low | 10 | 7 | 9 | 1 |
| 14 | female | 5.5 | Both | 5.7 | 2.3 | 3.05 | 1.3 | medium | 7 | 8 | 5 | 1 |
| 15 | female | 7.3 | Instagram | 4.1 | 2.1 | 2.87 | 0.4 | low | 10 | 10 | 1 | 1 |
| 19 | female | 7.4 | Both | 4.4 | 1.4 | 3.78 | 1.1 | low | 9 | 7 | 5 | 1 |
| 15 | female | 7.8 | Instagram | 4.6 | 3.0 | 2.44 | 1.4 | medium | 8 | 10 | 6 | 1 |
| 17 | male | 6.9 | Both | 4.6 | 2.5 | 2.04 | 0.8 | high | 10 | 9 | 2 | 1 |
| 18 | female | 6.3 | TikTok | 4.8 | 1.2 | 2.91 | 1.3 | medium | 9 | 10 | 3 | 1 |
| 19 | male | 8.0 | TikTok | 4.7 | 0.5 | 2.18 | 0.6 | medium | 8 | 8 | 6 | 1 |

#### **Nhận xét & Insight (Insights)**

- Đặc điểm nhận diện nổi bật nhất của nhóm học sinh bị trầm cảm (`depression_label = 1`) là họ sử dụng mạng xã hội với thời lượng cực kỳ lớn, tất cả 31 học sinh đều dùng ít nhất từ 5.1 giờ/ngày trở lên (nhiều bạn dùng tới 7-8 giờ/ngày).
- Đi kèm với đó, nhóm này có chỉ số căng thẳng (`stress_level`) và mức lo âu (`anxiety_level`) cực kỳ cao (tất cả đều từ 7 đến 10), đồng thời thời gian ngủ cũng rất ít (hầu hết đều dưới 6 tiếng).
- Nhìn chung, có mối liên hệ mật thiết giữa tình trạng bị trầm cảm với thói quen dùng mạng xã hội nhiều giờ liền cũng như chỉ số stress, lo âu và thiếu ngủ trầm trọng.
