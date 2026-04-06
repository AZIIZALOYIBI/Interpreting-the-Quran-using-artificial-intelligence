-- Seed initial categories
INSERT INTO categories (id, name_ar, name_en, icon, description, color, bg_color, text_color)
VALUES
    ('medicine', 'الطب والصحة', 'Medicine & Health', '🏥', 'الإرشاد القرآني في الصحة والعلاج', 'bg-green-600', 'bg-green-50', 'text-green-700'),
    ('work', 'العمل والمال', 'Work & Finance', '💼', 'التوجيه الإلهي في الرزق والكسب الحلال', 'bg-blue-600', 'bg-blue-50', 'text-blue-700'),
    ('science', 'العلوم والتكنولوجيا', 'Science & Technology', '🔬', 'الإعجاز العلمي في القرآن', 'bg-purple-600', 'bg-purple-50', 'text-purple-700'),
    ('family', 'الأسرة والمجتمع', 'Family & Society', '👨‍👩‍👧‍👦', 'منظومة الأسرة في الإسلام', 'bg-orange-600', 'bg-orange-50', 'text-orange-700'),
    ('self_development', 'التطوير الذاتي', 'Self Development', '🧠', 'بناء الشخصية المتكاملة', 'bg-yellow-600', 'bg-yellow-50', 'text-yellow-700'),
    ('law', 'القانون والعدالة', 'Law & Justice', '⚖️', 'منظومة العدل والحقوق في الشريعة', 'bg-red-600', 'bg-red-50', 'text-red-700'),
    ('environment', 'البيئة والطبيعة', 'Environment & Nature', '🌍', 'الحفاظ على البيئة وعمارة الأرض', 'bg-teal-600', 'bg-teal-50', 'text-teal-700'),
    ('chat', 'اسأل القرآن', 'Ask Quran', '💬', 'تحدث مباشرة مع المساعد الذكي', 'bg-emerald-600', 'bg-emerald-50', 'text-emerald-700')
ON CONFLICT (id) DO NOTHING;
