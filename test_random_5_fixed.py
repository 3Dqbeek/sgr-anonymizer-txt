#!/usr/bin/env python3
"""
Тестирование исправленной SGR системы на 5 случайных диалогах
"""

import os
import random
import logging
from datetime import datetime
from sgr_anonymizer.core_sgr_fixed import SGRFixedAnonymizer

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_random_5_dialogs():
    """Тестирует исправленную систему на 5 случайных диалогах"""
    
    input_dir = "dialog_in"
    output_dir = "dialog_test_fixed_random"
    
    # Создаем выходную директорию
    os.makedirs(output_dir, exist_ok=True)
    
    # Получаем список .txt файлов
    all_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    if len(all_files) < 5:
        logger.warning(f"Найдено только {len(all_files)} файлов, но требуется 5")
        selected_files = all_files
    else:
        # Выбираем 5 случайных файлов
        selected_files = random.sample(all_files, 5)
    
    logger.info(f"📁 Выбрано {len(selected_files)} случайных файлов для тестирования:")
    for i, filename in enumerate(selected_files, 1):
        logger.info(f"  {i}. {filename}")
    
    # Создаем анонимизатор
    try:
        anonymizer = SGRFixedAnonymizer()
        logger.info("✅ SGRFixedAnonymizer создан успешно")
    except Exception as e:
        logger.error(f"❌ Ошибка создания анонимизатора: {e}")
        return
    
    # Статистика
    total_files = len(selected_files)
    processed_files = 0
    total_replacements = 0
    total_fio = 0
    total_email = 0
    total_phone = 0
    total_address = 0
    total_passport = 0
    total_snils = 0
    total_inn = 0
    total_card = 0
    total_birth = 0
    total_family = 0
    total_ip = 0
    start_time = datetime.now()
    
    # Обрабатываем каждый файл
    for i, filename in enumerate(selected_files, 1):
        logger.info(f"\n{'='*70}")
        logger.info(f"[{i}/{total_files}] Обработка: {filename}")
        logger.info(f"{'='*70}")
        
        try:
            # Читаем файл
            input_path = os.path.join(input_dir, filename)
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"📏 Размер файла: {len(content)} символов")
            
            # Анонимизируем
            file_start_time = datetime.now()
            logger.info("🔄 Начинаем анонимизацию...")
            result = anonymizer.anonymize(content)
            file_end_time = datetime.now()
            
            # Сохраняем результат
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            
            # Подсчитываем замены
            replacements_count = result.count('[') - result.count('[[')
            
            # Статистика по типам замен
            fio_count = result.count('[ФИО]')
            email_count = result.count('[EMAIL]')
            phone_count = result.count('[ТЕЛЕФОН]')
            address_count = result.count('[АДРЕС]')
            passport_count = result.count('[ПАСПОРТ]')
            snils_count = result.count('[СНИЛС]')
            inn_count = result.count('[ИНН]')
            card_count = result.count('[НОМЕР КАРТЫ]')
            birth_count = result.count('[ДАТА РОЖДЕНИЯ]')
            family_count = result.count('[РОДСТВЕННАЯ СВЯЗЬ]')
            ip_count = result.count('[IP-АДРЕС]')
            
            total_replacements += replacements_count
            total_fio += fio_count
            total_email += email_count
            total_phone += phone_count
            total_address += address_count
            total_passport += passport_count
            total_snils += snils_count
            total_inn += inn_count
            total_card += card_count
            total_birth += birth_count
            total_family += family_count
            total_ip += ip_count
            
            processed_files += 1
            
            logger.info(f"✅ Успешно обработан")
            logger.info(f"🔄 Всего замен: {replacements_count}")
            logger.info(f"  - [ФИО]: {fio_count}")
            logger.info(f"  - [EMAIL]: {email_count}")
            logger.info(f"  - [ТЕЛЕФОН]: {phone_count}")
            logger.info(f"  - [АДРЕС]: {address_count}")
            logger.info(f"  - [ПАСПОРТ]: {passport_count}")
            logger.info(f"  - [СНИЛС]: {snils_count}")
            logger.info(f"  - [ИНН]: {inn_count}")
            logger.info(f"  - [НОМЕР КАРТЫ]: {card_count}")
            logger.info(f"  - [ДАТА РОЖДЕНИЯ]: {birth_count}")
            logger.info(f"  - [РОДСТВЕННАЯ СВЯЗЬ]: {family_count}")
            logger.info(f"  - [IP-АДРЕС]: {ip_count}")
            logger.info(f"⏱️ Время обработки: {(file_end_time - file_start_time).total_seconds():.2f} секунд")
            logger.info(f"💾 Результат сохранен: {output_path}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки файла {filename}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            continue
    
    # Финальная статистика
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    
    logger.info(f"\n{'='*70}")
    logger.info("📊 ИТОГОВАЯ СТАТИСТИКА:")
    logger.info(f"📁 Файлов обработано: {processed_files}/{total_files}")
    logger.info(f"🔄 Всего замен: {total_replacements}")
    logger.info(f"  - [ФИО]: {total_fio}")
    logger.info(f"  - [EMAIL]: {total_email}")
    logger.info(f"  - [ТЕЛЕФОН]: {total_phone}")
    logger.info(f"  - [АДРЕС]: {total_address}")
    logger.info(f"  - [ПАСПОРТ]: {total_passport}")
    logger.info(f"  - [СНИЛС]: {total_snils}")
    logger.info(f"  - [ИНН]: {total_inn}")
    logger.info(f"  - [НОМЕР КАРТЫ]: {total_card}")
    logger.info(f"  - [ДАТА РОЖДЕНИЯ]: {total_birth}")
    logger.info(f"  - [РОДСТВЕННАЯ СВЯЗЬ]: {total_family}")
    logger.info(f"  - [IP-АДРЕС]: {total_ip}")
    logger.info(f"⏱️ Общее время: {total_time:.2f} секунд")
    if processed_files > 0:
        logger.info(f"📈 Среднее время на файл: {total_time/processed_files:.2f} секунд")
        logger.info(f"📈 Среднее замен на файл: {total_replacements/processed_files:.2f}")
    logger.info(f"📤 Результаты сохранены в: {output_dir}/")
    logger.info(f"{'='*70}")
    logger.info("\n✅ Тестирование завершено!")
    logger.info("🔍 Проверьте качество в сохраненных файлах:")

if __name__ == "__main__":
    test_random_5_dialogs()






