//
// Package eprinttools is a collection of structures and functions for working with the E-Prints REST API
//
// @author R. S. Doiel, <rsdoiel@caltech.edu>
//
// Copyright (c) 2017, Caltech
// All rights not granted herein are expressly reserved by Caltech.
//
// Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
//
// 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
package eprinttools

import (
	"log"
	"os"
	"testing"
	"time"

	// Caltech Library packages
	"github.com/caltechlibrary/cli"
)

// cfg is configuration to access the EPrints REST API for tests
var (
	cfg *cli.Config
)

func TestListEPrintURI(t *testing.T) {
	_, err := ListEPrintURI()
	if err != nil {
		t.Errorf("listEPrintURI() %s", err)
	}

	start, _ := time.Parse("2006-01-02", "2017-06-01")
	end, _ := time.Parse("2006-01-02", "2017-06-02")
	uris, err := ListModifiedEPrintURI(start, end)
	if err != nil {
		t.Errorf("listEPrintURI() %s", err)
	}
	log.Printf("DEBUG uri: %+v\n", uris)
}

func TestMain(m *testing.M) {
	cfg = cli.New("ep", "EP", "", Version)
	cfg.MergeEnv("eprint_url", "")
	cfg.MergeEnv("dataset", "")
	cfg.MergeEnv("htdocs", "")
	os.Exit(m.Run())
}