"""
Тесты для модуля загрузки документов.
"""

import pytest
import tempfile
import json
from pathlib import Path
from typing import List

from src.rag.document_loader import DocumentLoader, LoaderResult


class TestDocumentLoader:
    """Тесты для DocumentLoader."""
    
    def setup_method(self):
        """Настройка перед каждым тестом."""
        self.loader = DocumentLoader()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def test_load_json_file_success(self):
        """Тест успешной загрузки JSON файла."""
        # Создаем тестовый JSON файл
        test_data = [
            {"id": 1, "name": "Test Program", "cost": 100000},
            {"id": 2, "name": "Another Program", "cost": 150000}
        ]
        
        json_file = self.temp_dir / "test.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # Загружаем файл
        results = self.loader.load_json_file(json_file)
        
        # Проверяем результат
        assert len(results) == 2
        assert all(r.success for r in results)
        assert all(r.source == "test" for r in results)
        assert "Test Program" in results[0].text
        assert "100000" in results[0].text
    
    def test_load_json_file_invalid(self):
        """Тест загрузки некорректного JSON файла."""
        # Создаем некорректный JSON файл
        json_file = self.temp_dir / "invalid.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write('{"invalid": json}')
        
        # Загружаем файл
        results = self.loader.load_json_file(json_file)
        
        # Проверяем результат
        assert len(results) == 1
        assert not results[0].success
        assert "Ошибка парсинга JSON" in results[0].error
    
    def test_load_txt_file_success(self):
        """Тест успешной загрузки TXT файла."""
        # Создаем тестовый TXT файл
        txt_content = "Это тестовый текстовый файл.\nВторая строка текста."
        txt_file = self.temp_dir / "test.txt"
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        
        # Загружаем файл
        results = self.loader.load_txt_file(txt_file)
        
        # Проверяем результат
        assert len(results) == 1
        assert results[0].success
        assert results[0].source == "test"
        assert "тестовый текстовый файл" in results[0].text
    
    def test_load_txt_file_empty(self):
        """Тест загрузки пустого TXT файла."""
        # Создаем пустой TXT файл
        txt_file = self.temp_dir / "empty.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        # Загружаем файл
        results = self.loader.load_txt_file(txt_file)
        
        # Проверяем результат
        assert len(results) == 1
        assert not results[0].success
        assert "Файл пустой" in results[0].error
    
    def test_load_directory_mixed_files(self):
        """Тест загрузки директории со смешанными форматами файлов."""
        # Создаем JSON файл
        json_data = [{"id": 1, "title": "JSON Document"}]
        json_file = self.temp_dir / "data.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False)
        
        # Создаем TXT файл
        txt_file = self.temp_dir / "info.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("Text document content")
        
        # Создаем неподдерживаемый файл
        other_file = self.temp_dir / "data.xml"
        with open(other_file, 'w', encoding='utf-8') as f:
            f.write("<xml>content</xml>")
        
        # Загружаем директорию
        results = self.loader.load_directory(self.temp_dir)
        
        # Проверяем результат
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]
        
        assert len(successful_results) == 2  # JSON + TXT
        assert len(failed_results) == 1     # XML (неподдерживаемый)
        
        sources = {r.source for r in successful_results}
        assert "data" in sources
        assert "info" in sources
    
    def test_get_statistics(self):
        """Тест получения статистики загрузки."""
        results = [
            LoaderResult("doc1", "Text content 1", success=True),
            LoaderResult("doc2", "Text content 2", success=True),
            LoaderResult("doc3", "", success=False, error="Test error")
        ]
        
        stats = self.loader.get_statistics(results)
        
        assert stats["total_documents"] == 3
        assert stats["successful"] == 2
        assert stats["failed"] == 1
        assert stats["total_characters"] == len("Text content 1Text content 2")
        assert len(stats["errors"]) == 1
        assert stats["errors"][0]["source"] == "doc3"
    
    def test_unsupported_file_type(self):
        """Тест обработки неподдерживаемого типа файла."""
        # Создаем файл с неподдерживаемым расширением
        xml_file = self.temp_dir / "data.xml"
        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write("<root>content</root>")
        
        # Пытаемся загрузить файл
        results = self.loader.load_file(xml_file)
        
        # Проверяем результат
        assert len(results) == 1
        assert not results[0].success
        assert "Неподдерживаемый формат файла" in results[0].error


@pytest.mark.integration
class TestDocumentLoaderIntegration:
    """Интеграционные тесты для DocumentLoader."""
    
    def test_load_real_seed_data(self):
        """Тест загрузки реальных seed данных."""
        from src.app.config import settings
        
        data_path = Path(settings.DATA_DIR)
        if not data_path.exists():
            pytest.skip("Директория seed данных не найдена")
        
        loader = DocumentLoader()
        results = loader.load_directory(data_path)
        
        # Проверяем что хотя бы один файл загружен успешно
        successful_results = [r for r in results if r.success]
        assert len(successful_results) > 0
        
        # Проверяем что есть непустой текст
        assert any(len(r.text) > 50 for r in successful_results)
        
        # Выводим статистику для отладки
        stats = loader.get_statistics(results)
        print(f"Загружено документов: {stats}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])