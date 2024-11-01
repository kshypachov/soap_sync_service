import logging

# створюється екземпляр класу logger
logger = logging.getLogger(__name__)


def log_element(element, indent=0):

    indent = indent + 1
    indent_str = "  " * indent

    tag = element.tag.split('}')[-1]  # Прибираємо простір імен
    text = element.text.strip() if element.text else ''
    logger.info(f"{indent_str}Tag: {tag}, Text: {text}")

    for child in element.iterchildren():
        log_element(child, indent)


def log_soap_headers(ctx):
    if ctx.in_header_doc is not None:
        logger.info("Logging SOAP headers:")
        for header in ctx.in_header_doc:
            log_element(element=header)
