//# Plano de Implementação Detalhado: Upload de Imagens para ImgBB

## Visão Geral

Este documento detalha a implementação do serviço de upload de imagens para o ImgBB, permitindo que as imagens sejam hospedadas externamente e referenciadas por URL.

---

## Fase 1: Preparação do Schema do Banco de Dados

### 1.1 Script de Migração

Criar arquivo: `database/migrations/002_add_imagem_remota.sql`

```sql
-- Migration: Adicionar campos para imagens remotas
-- Versão: 002
-- Data: 2026-02-03

-- Adicionar colunas à tabela imagem
ALTER TABLE imagem ADD COLUMN url_remota VARCHAR(1000);
ALTER TABLE imagem ADD COLUMN servico_hospedagem VARCHAR(50);
ALTER TABLE imagem ADD COLUMN id_remoto VARCHAR(255);
ALTER TABLE imagem ADD COLUMN url_thumbnail VARCHAR(1000);
ALTER TABLE imagem ADD COLUMN data_upload_remoto DATETIME;

-- Índice para busca por URL (performance)
CREATE INDEX IF NOT EXISTS idx_imagem_url_remota ON imagem(url_remota);
CREATE INDEX IF NOT EXISTS idx_imagem_servico ON imagem(servico_hospedagem);
```

### 1.2 Atualizar Model ORM

Modificar: `src/models/orm/imagem.py`

Adicionar os novos campos:
- `url_remota: Optional[str]` - URL pública da imagem
- `servico_hospedagem: Optional[str]` - Nome do serviço (imgbb, cloudinary, s3)
- `id_remoto: Optional[str]` - ID da imagem no serviço externo
- `url_thumbnail: Optional[str]` - URL do thumbnail (se disponível)
- `data_upload_remoto: Optional[datetime]` - Data do upload remoto

Adicionar métodos:
- `tem_url_remota() -> bool` - Verifica se a imagem tem URL externa
- `get_url_para_exibicao() -> str` - Retorna URL remota ou caminho local

---

## Fase 2: Criar Estrutura de Serviços de Upload

### 2.1 Estrutura de Diretórios

```
src/
├── services/
│   └── image_upload/
│       ├── __init__.py
│       ├── base_uploader.py       # Interface abstrata
│       ├── upload_result.py       # Dataclass de resultado
│       ├── imgbb_uploader.py      # Implementação ImgBB
│       ├── local_uploader.py      # Fallback local
│       └── uploader_factory.py    # Factory para selecionar serviço
```

### 2.2 Arquivo: `upload_result.py`

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class UploadResult:
    """Resultado de uma operação de upload"""
    success: bool
    url: Optional[str] = None
    url_thumbnail: Optional[str] = None
    url_medium: Optional[str] = None
    id_remoto: Optional[str] = None
    servico: Optional[str] = None
    delete_url: Optional[str] = None
    erro: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
```

### 2.3 Arquivo: `base_uploader.py`

```python
from abc import ABC, abstractmethod
from typing import Optional
from .upload_result import UploadResult

class BaseImageUploader(ABC):
    """Interface abstrata para serviços de upload de imagem"""

    @property
    @abstractmethod
    def nome_servico(self) -> str:
        """Nome identificador do serviço"""
        pass

    @abstractmethod
    def upload(self, caminho_arquivo: str, nome: Optional[str] = None) -> UploadResult:
        """
        Faz upload da imagem e retorna resultado

        Args:
            caminho_arquivo: Caminho local do arquivo
            nome: Nome customizado (opcional)

        Returns:
            UploadResult com URL ou erro
        """
        pass

    @abstractmethod
    def delete(self, id_remoto: str) -> bool:
        """
        Remove imagem do serviço externo

        Args:
            id_remoto: ID da imagem no serviço

        Returns:
            True se removido com sucesso
        """
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """
        Verifica se o serviço está configurado corretamente

        Returns:
            True se as credenciais estão configuradas
        """
        pass

    def validate_file(self, caminho_arquivo: str) -> tuple[bool, str]:
        """
        Valida se o arquivo pode ser enviado

        Returns:
            Tupla (válido, mensagem_erro)
        """
        import os

        if not os.path.exists(caminho_arquivo):
            return False, "Arquivo não encontrado"

        # Verificar extensão
        extensoes_validas = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        ext = os.path.splitext(caminho_arquivo)[1].lower()
        if ext not in extensoes_validas:
            return False, f"Extensão {ext} não suportada"

        # Verificar tamanho (max 32MB para ImgBB)
        tamanho = os.path.getsize(caminho_arquivo)
        if tamanho > 32 * 1024 * 1024:
            return False, "Arquivo maior que 32MB"

        return True, ""
```

### 2.4 Arquivo: `imgbb_uploader.py`

```python
import base64
import requests
import logging
from typing import Optional
from .base_uploader import BaseImageUploader
from .upload_result import UploadResult

logger = logging.getLogger(__name__)

class ImgBBUploader(BaseImageUploader):
    """Implementação do uploader para ImgBB"""

    API_URL = "https://api.imgbb.com/1/upload"
    TIMEOUT = 30  # segundos

    def __init__(self, api_key: str):
        self._api_key = api_key

    @property
    def nome_servico(self) -> str:
        return "imgbb"

    def is_configured(self) -> bool:
        return bool(self._api_key and len(self._api_key) > 10)

    def upload(self, caminho_arquivo: str, nome: Optional[str] = None) -> UploadResult:
        """Faz upload da imagem para ImgBB"""

        # Validar arquivo
        valido, erro = self.validate_file(caminho_arquivo)
        if not valido:
            return UploadResult(success=False, erro=erro, servico=self.nome_servico)

        # Verificar configuração
        if not self.is_configured():
            return UploadResult(
                success=False,
                erro="API key do ImgBB não configurada",
                servico=self.nome_servico
            )

        try:
            # Ler e codificar imagem em base64
            with open(caminho_arquivo, "rb") as f:
                imagem_base64 = base64.b64encode(f.read()).decode("utf-8")

            # Preparar payload
            payload = {
                "key": self._api_key,
                "image": imagem_base64,
            }

            if nome:
                payload["name"] = nome

            # Fazer requisição
            logger.info(f"Iniciando upload para ImgBB: {caminho_arquivo}")
            response = requests.post(
                self.API_URL,
                data=payload,
                timeout=self.TIMEOUT
            )

            # Processar resposta
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    img_data = data["data"]
                    logger.info(f"Upload bem-sucedido. ID: {img_data['id']}")

                    return UploadResult(
                        success=True,
                        url=img_data["url"],
                        url_thumbnail=img_data.get("thumb", {}).get("url"),
                        url_medium=img_data.get("medium", {}).get("url"),
                        id_remoto=img_data["id"],
                        delete_url=img_data.get("delete_url"),
                        servico=self.nome_servico
                    )
                else:
                    erro = data.get("error", {}).get("message", "Erro desconhecido")
                    logger.error(f"Erro no upload: {erro}")
                    return UploadResult(success=False, erro=erro, servico=self.nome_servico)
            else:
                erro = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"Erro HTTP no upload: {erro}")
                return UploadResult(success=False, erro=erro, servico=self.nome_servico)

        except requests.Timeout:
            logger.error("Timeout no upload para ImgBB")
            return UploadResult(
                success=False,
                erro="Timeout - servidor não respondeu",
                servico=self.nome_servico
            )
        except requests.RequestException as e:
            logger.error(f"Erro de conexão: {e}")
            return UploadResult(
                success=False,
                erro=f"Erro de conexão: {str(e)}",
                servico=self.nome_servico
            )
        except Exception as e:
            logger.exception(f"Erro inesperado no upload: {e}")
            return UploadResult(
                success=False,
                erro=f"Erro inesperado: {str(e)}",
                servico=self.nome_servico
            )

    def delete(self, id_remoto: str) -> bool:
        """
        ImgBB não oferece API de deleção via ID.
        A deleção deve ser feita via delete_url (se salva)
        """
        logger.warning("ImgBB não suporta deleção via API. Use delete_url manualmente.")
        return False
```

### 2.5 Arquivo: `local_uploader.py`

```python
import os
import shutil
import uuid
from typing import Optional
from .base_uploader import BaseImageUploader
from .upload_result import UploadResult

class LocalUploader(BaseImageUploader):
    """Uploader local (fallback) - comportamento atual do sistema"""

    def __init__(self, diretorio_base: str):
        self._diretorio_base = diretorio_base

    @property
    def nome_servico(self) -> str:
        return "local"

    def is_configured(self) -> bool:
        return os.path.isdir(self._diretorio_base)

    def upload(self, caminho_arquivo: str, nome: Optional[str] = None) -> UploadResult:
        """Copia imagem para diretório local"""

        valido, erro = self.validate_file(caminho_arquivo)
        if not valido:
            return UploadResult(success=False, erro=erro, servico=self.nome_servico)

        try:
            # Gerar nome único
            ext = os.path.splitext(caminho_arquivo)[1]
            nome_final = nome or f"{uuid.uuid4().hex}{ext}"
            destino = os.path.join(self._diretorio_base, nome_final)

            # Copiar arquivo
            shutil.copy2(caminho_arquivo, destino)

            return UploadResult(
                success=True,
                url=destino,  # Caminho local como "URL"
                id_remoto=nome_final,
                servico=self.nome_servico
            )
        except Exception as e:
            return UploadResult(
                success=False,
                erro=str(e),
                servico=self.nome_servico
            )

    def delete(self, id_remoto: str) -> bool:
        """Remove arquivo local"""
        try:
            caminho = os.path.join(self._diretorio_base, id_remoto)
            if os.path.exists(caminho):
                os.remove(caminho)
                return True
            return False
        except Exception:
            return False
```

### 2.6 Arquivo: `uploader_factory.py`

```python
import configparser
import logging
from typing import Optional
from .base_uploader import BaseImageUploader
from .imgbb_uploader import ImgBBUploader
from .local_uploader import LocalUploader

logger = logging.getLogger(__name__)

class UploaderFactory:
    """Factory para criar o uploader apropriado baseado na configuração"""

    @staticmethod
    def criar_uploader(config_path: str = "config.ini") -> BaseImageUploader:
        """
        Cria o uploader baseado na configuração

        Args:
            config_path: Caminho para o arquivo de configuração

        Returns:
            Instância do uploader configurado
        """
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        # Ler serviço configurado
        servico = config.get("IMAGES", "upload_service", fallback="local")
        logger.info(f"Serviço de upload configurado: {servico}")

        if servico == "imgbb":
            api_key = config.get("IMGBB", "api_key", fallback="")
            uploader = ImgBBUploader(api_key)

            if uploader.is_configured():
                logger.info("ImgBB configurado com sucesso")
                return uploader
            else:
                logger.warning("ImgBB não configurado, usando fallback local")

        # Fallback para local
        images_dir = config.get("PATHS", "images_dir", fallback="imagens")
        return LocalUploader(images_dir)

    @staticmethod
    def criar_uploader_por_nome(nome: str, config_path: str = "config.ini") -> Optional[BaseImageUploader]:
        """
        Cria um uploader específico pelo nome

        Args:
            nome: Nome do serviço (imgbb, local)
            config_path: Caminho para o arquivo de configuração
        """
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        if nome == "imgbb":
            api_key = config.get("IMGBB", "api_key", fallback="")
            return ImgBBUploader(api_key)
        elif nome == "local":
            images_dir = config.get("PATHS", "images_dir", fallback="imagens")
            return LocalUploader(images_dir)

        return None
```

### 2.7 Arquivo: `__init__.py`

```python
"""
Serviços de Upload de Imagens

Módulo responsável pelo upload de imagens para serviços externos
(ImgBB, Cloudinary, S3) ou armazenamento local.
"""

from .upload_result import UploadResult
from .base_uploader import BaseImageUploader
from .imgbb_uploader import ImgBBUploader
from .local_uploader import LocalUploader
from .uploader_factory import UploaderFactory

__all__ = [
    "UploadResult",
    "BaseImageUploader",
    "ImgBBUploader",
    "LocalUploader",
    "UploaderFactory"
]
```

---

## Fase 3: Atualizar Configuração

### 3.1 Adicionar seção no `config.ini`

```ini
[IMAGES]
# Serviço de upload: local, imgbb
upload_service = local
# Formatos de imagem suportados
supported_formats = png,jpg,jpeg,svg
# Tamanho máximo de imagem em MB
max_size_mb = 10
# Escala padrão para LaTeX
default_scale = 0.7

[IMGBB]
# API Key do ImgBB (obter em https://api.imgbb.com/)
api_key =
```

---

## Fase 4: Atualizar Repository

### 4.1 Modificar `src/repositories/imagem_repository.py`

Adicionar métodos:
- `upload_para_servico_externo(uuid: str) -> UploadResult` - Faz upload de imagem existente
- `buscar_por_url_remota(url: str) -> Optional[Imagem]` - Busca por URL
- `atualizar_url_remota(uuid: str, result: UploadResult)` - Atualiza dados remotos
- `listar_sem_url_remota() -> List[Imagem]` - Lista imagens locais não sincronizadas
- `sincronizar_todas_para_remoto() -> dict` - Upload em lote

---

## Fase 5: Integrar com ImagePicker (UI)

### 5.1 Modificar componente de seleção de imagem

Arquivo: `src/views/components/forms/image_picker.py` (ou similar)

- Adicionar checkbox "Fazer upload para serviço externo"
- Mostrar status do upload (loading, sucesso, erro)
- Exibir URL remota após upload bem-sucedido
- Opção de copiar URL para clipboard

### 5.2 Fluxo de Upload na UI

```
1. Usuário seleciona imagem local
2. Sistema calcula hash MD5 (deduplicação)
3. Sistema salva localmente (backup)
4. Se upload_service != local:
   a. Mostra indicador de progresso
   b. Faz upload para serviço externo
   c. Salva URL no banco
   d. Mostra confirmação com URL
5. Referencia imagem na questão/alternativa
```

---

## Fase 6: Atualizar Exibição de Imagens

### 6.1 Lógica de Exibição

Em todo lugar que exibe imagens, usar a seguinte lógica:

```python
def get_caminho_imagem(imagem: Imagem) -> str:
    """Retorna o melhor caminho para exibir a imagem"""
    if imagem.url_remota:
        return imagem.url_remota
    return imagem.caminho_relativo
```

### 6.2 Atualizar Preview de Questões

Modificar `src/views/pages/questao_preview_page.py` para usar URLs quando disponíveis.

### 6.3 Atualizar Export LaTeX

Modificar `src/controllers/export_controller.py`:
- Se imagem tem URL remota, usar `\includegraphics` com download automático
- OU fazer download para pasta temporária antes da compilação

---

## Fase 7: Adicionar Dependências

### 7.1 Atualizar `requirements.txt`

```txt
# Upload de imagens
requests>=2.28.0
```

---

## Fase 8: Testes

### 8.1 Testes Unitários

Criar: `tests/test_image_upload/`

- `test_imgbb_uploader.py` - Mock da API do ImgBB
- `test_local_uploader.py` - Testes de upload local
- `test_uploader_factory.py` - Testes da factory

### 8.2 Testes de Integração

- Testar upload real para ImgBB (com API key de teste)
- Testar fallback quando serviço indisponível
- Testar deduplicação (não reupload de imagem já existente)

---

## Checklist de Implementação

### Fase 1 - Schema
- [ ] Criar migration SQL
- [ ] Executar migration no banco de desenvolvimento
- [ ] Atualizar model `Imagem` com novos campos
- [ ] Testar que campos são salvos corretamente

### Fase 2 - Serviços
- [ ] Criar estrutura de diretórios
- [ ] Implementar `UploadResult`
- [ ] Implementar `BaseImageUploader`
- [ ] Implementar `ImgBBUploader`
- [ ] Implementar `LocalUploader`
- [ ] Implementar `UploaderFactory`
- [ ] Criar `__init__.py` com exports

### Fase 3 - Configuração
- [ ] Adicionar seção `[IMGBB]` no config.ini
- [ ] Atualizar seção `[IMAGES]` com `upload_service`
- [ ] Documentar como obter API key

### Fase 4 - Repository
- [ ] Adicionar métodos no `ImagemRepository`
- [ ] Testar upload e atualização de URL

### Fase 5 - UI
- [ ] Atualizar `ImagePicker` com opção de upload remoto
- [ ] Adicionar indicador de progresso
- [ ] Tratar erros de upload

### Fase 6 - Exibição
- [ ] Atualizar preview de questões
- [ ] Atualizar export LaTeX

### Fase 7 - Dependências
- [ ] Adicionar `requests` ao requirements.txt
- [ ] Testar instalação em ambiente limpo

### Fase 8 - Testes
- [ ] Criar testes unitários
- [ ] Criar testes de integração
- [ ] Testar em cenário real

---

## API do ImgBB - Referência

### Endpoint de Upload
```
POST https://api.imgbb.com/1/upload
```

### Parâmetros
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| key | string | Sim | API key |
| image | string | Sim | Imagem em base64 |
| name | string | Não | Nome da imagem |
| expiration | integer | Não | Tempo em segundos para expirar |

### Resposta de Sucesso
```json
{
  "data": {
    "id": "abc123",
    "title": "nome_imagem",
    "url": "https://i.ibb.co/abc123/imagem.png",
    "display_url": "https://i.ibb.co/abc123/imagem.png",
    "delete_url": "https://ibb.co/abc123/remove",
    "thumb": {
      "url": "https://i.ibb.co/abc123/imagem-thumb.png"
    },
    "medium": {
      "url": "https://i.ibb.co/abc123/imagem-medium.png"
    }
  },
  "success": true,
  "status": 200
}
```

### Obter API Key
1. Acessar https://api.imgbb.com/
2. Criar conta ou fazer login
3. Clicar em "Get API Key"
4. Copiar a chave gerada
5. Colar no `config.ini` na seção `[IMGBB]`

---

## Considerações de Segurança

1. **API Key**: Nunca versionar a API key. Usar `.gitignore` para `config.ini` local ou variáveis de ambiente.

2. **Backup Local**: Sempre manter cópia local das imagens, mesmo após upload bem-sucedido.

3. **Validação**: Validar tipo e tamanho do arquivo antes do upload.

4. **Rate Limiting**: ImgBB tem limite de 60 uploads por hora no plano gratuito.

5. **Persistência**: URLs do ImgBB são permanentes (não expiram por padrão).

---

*Documento criado em: 2026-02-03*
*Autor: Sistema de Planejamento*
