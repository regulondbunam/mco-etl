configfile: "config/config.json"
conf_url= config["url"]
conf_db= config["db"]
conf_organism = config["organism"]
conf_version = config["version"]
conf_source = config ["source"]
conf_source_version = config ["source_version"]
data_upload_config = config["data_upload_config"]
'''
rule all:
    input:
        "logs/mco_et_log/mco_et_log.log",
        
        # Release Modules log files
        "logs/schema_loader_log/schema_loader_log.log",
        "logs/validation_log/validation_log.log",
        "logs/create_identifiers_log/create_identifiers_log.log",
        "logs/re_validation_log/validation_log.log",
        "logs/replace_identifiers_log/replace_identifiers_log.log",
        "logs/data_uploader_log/data_uploader_log.log"

rule mcoet:
    params:
        main_path = "mco_etl/",
        schema_version = 1.0
    input:
        ontology = "input_files/mco-edit.owl"
    output:
        terms = "output_files/terms.json",
        ontology_metadata = "output_files/ontologies.json",
        log = "logs/mco_et_log/mco_et_log.log"
    log:
        "logs/mco_et_log/mco_et_log.log"
    conda:
        "envs/et_tools.yaml"
    priority: 10
    shell:
        "python {params.main_path} -i {input.ontology} -o {output.terms} -m {output.ontology_metadata} -s {params.schema_version} -l {output.log}"

rule schema_loader:
    # DO NOT USE
    params:
        main_path = "release_modules/schema_loader/",
        db = {conf_db},
        url = {conf_url},
        schemas = "schemas/json_schemas",
        log = "logs/schema_loader_log"
    log:
        "logs/schema_loader_log/schema_loader_log.log"
    conda:
        "envs/db_dependencies.yaml"
    priority: 9
    shell:
        "python {params.main_path} -db {params.db} -u {params.url} -s {params.schemas} -l {params.log} -d"

rule data_validator:
    params:
        main_path = "data-release-tools/src/data_validator/",
        data = "output_files/",
        schemas = "schemas/json_schemas",
        valid_data = "valid_data/",
        invalid_data = "invalid_data/",
        log = "logs/validation_log/"
    log:
        "logs/validation_log/validation_log.log"
    conda:
        "envs/py_down_grade.yaml"
    priority: 8
    shell:
        "python {params.main_path} -i {params.data} -s {params.schemas} -v {params.valid_data} -iv {params.invalid_data} -l {params.log} -sp"

rule create_identifiers:
    params:
        main_path = "data-release-tools/src/create_identifiers/",
        db = {conf_db},
        url = {conf_url},
        valid_data = "valid_data/",
        organism = {conf_organism},
        version = {conf_version},
        source = {conf_source},
        source_version = {conf_source_version},
        log = "logs/create_identifiers_log/"
    log:
        "logs/create_identifiers_log/create_identifiers_log.log"
    conda:
        "envs/db_dependencies.yaml"
    priority: 7
    shell:
        'python3 {params.main_path} -u {params.url} -i {params.valid_data} -org {params.organism} -s {params.source} -sv {params.source_version} -v {params.version} -db "{params.db}" -l {params.log}'
     
rule replace_identifiers:
    params:
        main_path = "data-release-tools/src/replace_identifiers/",
        organism = {conf_organism},
        valid_data = "valid_data/",
        replaced_ids = "replaced_ids/",
        version = {conf_version},
        db = {conf_db},
        url = {conf_url},
        log = "logs/replace_identifiers_log/"
    log:
        "logs/replace_identifiers_log/replace_identifiers_log.log"
    conda:
        "envs/db_dependencies.yaml"
    priority: 6
    shell:
        "python {params.main_path} -org {params.organism} -i {params.valid_data} -o {params.replaced_ids} -u {params.url} -v {params.version} -db {params.db} -l {params.log}"        

rule re_validate_data:
    params:
        main_path = "data-release-tools/src/data_validator/",
        data = "replaced_ids/",
        schemas = "schemas/json_schemas",
        valid_data = "replaced_valid_data/",
        invalid_data = "invalid_data/",
        log = "logs/re_validation_log/"
    log:
        "logs/re_validation_log/validation_log.log"
    conda:
        "envs/py_down_grade.yaml"
    priority: 5
    shell:
        "python {params.main_path} -i {params.data} -s {params.schemas} -v {params.valid_data} -iv {params.invalid_data} -l {params.log}"

rule data_uploader:
    params:
        main_path = "data-release-tools/src/data_uploader/",
        valid_data = "replaced_valid_data/",
        url = {conf_url},
        log = "logs/data_uploader_log/"
    log:
        "logs/data_uploader_log/data_uploader_log.log"
    conda:
        "envs/db_dependencies.yaml"
    priority: 4
    shell:
        "python {params.main_path} -i {params.valid_data} -u {params.url} -mg -l {params.log}"

'''
rule data_uploader:
    params:
        main_path = "../../../../Libs/data-release-tools/src/data_uploader/",
        valid_data = "replaced_ids/",
        log = data_upload_config["log_dir"],
        db = config["db"],
        url = config["url"]
    log:
        "logs/data_uploader_log/data_uploader_log.log"
    conda:
        "envs/db_dependencies.yaml"
    priority: 4
    shell:
        "python {params.main_path} -i {params.valid_data} -u {params.url} -db {params.db} -l {params.log}"
