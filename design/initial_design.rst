Standard:
    PEP8
    Travis CI
    Sphinx docstrings
    Type Hints
    Docstrings on every function/class
    Reviewers for each pull request

    "ID/BLOCK_SUBBLOCK_feature"
    e.g:
        if Marcelo Lerendegui is working adding a filter to the image processing core of the server: 
            git checkout -b "ml/SERVER_IMC_add_filter"

TODO:
Doc
    README                      (Marcelo)
    Sphinx doc                  (Marcelo)

Setup Travis-CI                 (Marcelo)

Project Structure               (Marcelo)

Client
    GUI                         (Willy)
        Design                  (Willy, Yihang, Marcelo)
        Draw                    (Willy)
        Assign Callbacks        (Willy)

    Api Calls
        Define Protocol         (Willy, Yihang, Marcelo)

    Integration Tests           (Willy, Yihang, Marcelo)

Server
    Database                    (Yihang)
        Online MongoDB Setup    (Yihang)
        Design                  (Willy, Yihang, Marcelo)
        Implement Model         (Yihang)
        Implement calls         (Yihang)
        Unit Tests              (Yihang)

    Views                       (Marcelo)
        Define Protocol         (Willy, Yihang, Marcelo)
    
    Image Processing Core
        Implement               (Marcelo)
        Unit Tests              (Marcelo)
    Api                         (Marcelo)
        Implement               (Marcelo)
        Unit Tests              (Marcelo)
    Validation                  (Marcelo)
        Implement               (Marcelo)
        Unit Tests              (Marcelo)

    Integration Tests           (Willy, Yihang, Marcelo)
