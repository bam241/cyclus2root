{
gROOT->Reset();
gStyle->SetOptStat(0);


TFile *FC1 = new TFile("cyclus_exp2_stat.root");
TT->SetMarkerStyle(7);

// ################################################################################
// Plutonium
// ################################################################################

    TCanvas *C0 = new TCanvas("C0","Pu",1500,450);
    C0->Divide(2,1,0.01,0.01);
        
    C0->cd(1);
    TT->Draw("B93:BU_UOX","T==100","");
    tmp0 = (TH1F*)gPad->GetPrimitive("htemp"); tmp0->SetTitle("Total Pu at E.O.S.");
    tmp0->GetXaxis()->SetTitle("BU UOX (GWd/t)");    tmp0->GetXaxis()->CenterTitle();    tmp0->GetXaxis()->SetTitleOffset(0.8);  tmp0->GetXaxis()->SetTitleSize(0.05);
    tmp0->GetYaxis()->SetTitle("Mass (tons)"); tmp0->GetYaxis()->CenterTitle();    tmp0->GetYaxis()->SetTitleOffset(0.8);  tmp0->GetYaxis()->SetTitleSize(0.05);
    gPad->Update();
    
    C0->cd(2);
    TT->Draw("B93:PSpec","T==100","");
    tmp0 = (TH1F*)gPad->GetPrimitive("htemp"); tmp0->SetTitle("Total Pu at E.O.S.");
    tmp0->GetXaxis()->SetTitle("Specific Power (W/g)");    tmp0->GetXaxis()->CenterTitle();    tmp0->GetXaxis()->SetTitleOffset(0.8);  tmp0->GetXaxis()->SetTitleSize(0.05);
    tmp0->GetYaxis()->SetTitle("Mass (tons)"); tmp0->GetYaxis()->CenterTitle();    tmp0->GetYaxis()->SetTitleOffset(0.8);  tmp0->GetYaxis()->SetTitleSize(0.05);
    gPad->Update();

    return 0;
}
