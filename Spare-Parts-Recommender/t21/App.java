package t21;

import java.util.InputMismatchException;
import java.util.Scanner;

public class App
{   protected static String[] partsName = new String[253];
    private static String brand;
    private static int productionYear;
    private static String model;
    GPT3Integration gpt3 = new GPT3Integration();

    public App() {
        brand = "";
        productionYear = 0;
        model = "";
        partsName[0] = "1.1  UPPER CONTROL ARM";
        partsName[1] = "1.2  UPPER BALL JOINT";
        partsName[2] = "1.3  COIL SPRING";
        partsName[3] = "1.4  SNOCK ABSORBER";
        partsName[4] = "1.5  LOWER BALL JOINT";
        partsName[5] = "1.6  LOWER CONTROL ARM";
        partsName[6] = "1.7  CONTROL ARM BUSHINGS";
        partsName[7] = "1.8  STABILIZER LINK";
        partsName[8] = "1.9  IDLER ARM";
        partsName[9] = "1.10 INNER TIE-ROD END";
        partsName[10] = "1.11 CENTER LINK";
        partsName[11] = "1.12 PITMAN ARM";
        partsName[12] = "1.13 ADJUSTING SLEEVE";
        partsName[13] = "1.14 OUTER TIE-ROD END";
        partsName[14] = "1.15 STEERING KNUCKLE";
        partsName[15] = "1.16 POWER STEERING PUMP";
        partsName[16] = "1.17 POWER STEERING GEARBOX";
        partsName[17] = "1.18 ANTI-SWAY BAR";
        partsName[18] = "1.19 BALL JOINT";
        partsName[19] = "1.20 UPPER MOUNTING PLATE-BEARING";
        partsName[20] = "1.21 MACPHERSON STRUT";
        partsName[21] = "1.22 BELLOWS";
        partsName[22] = "1.23 RACK-PINION UNIT";
        partsName[23] = "1.24 RACK-PINION BUSHINGS";
        partsName[24] = "1.25 INNER SCOKET ASSEMBLY";
        partsName[25] = "1.26 WHEEL HUB";
        partsName[26] = "1.27 WHEEL BEARING";
        partsName[27] = "1.28 POWER STEERING";
        partsName[28] = "2.1  SPIGOT BEARING";
        partsName[29] = "2.2  RETAINING SPRING WITH PREFORMED FINGERS";
        partsName[30] = "2.3  RELEAS RING";
        partsName[31] = "2.4  RETAINING SPRING";
        partsName[32] = "2.5  BALL PIN FOR CLUCH FORK";
        partsName[33] = "2.6  FLYWHEEL";
        partsName[34] = "2.7  DRIVE DISC";
        partsName[35] = "2.8  PRESSURE PLATE";
        partsName[36] = "2.9  INNER FULCRUM RING";
        partsName[37] = "2.10 OUTER FULCRUM RING";
        partsName[38] = "2.11 CLUTCH COVER";
        partsName[39] = "2.12 RELEASE FORK";
        partsName[40] = "2.13 RETURN SPRING OF RELEASE FORK";
        partsName[41] = "2.14 RELEASE BEARING";
        partsName[42] = "2.15 DIAPHRAGM SPRING";
        partsName[43] = "2.16 PILOT BUSHING";
        partsName[44] = "2.17 BELLHOUSING";
        partsName[45] = "3.1  FUEL PUMP";
        partsName[46] = "3.2  CYLINDER HEAD COVER";
        partsName[47] = "3.3  GASKET";
        partsName[48] = "3.4  THERMOSTAT COVER AND GASKET";
        partsName[49] = "3.5  THERMOSTAT";
        partsName[50] = "3.6  HEAT GAUGE UNIT";
        partsName[51] = "3.7  BRACKET";
        partsName[52] = "3.8  ROCKER ARM AND SHAFT ASSEMBLE";
        partsName[53] = "3.9  ROCKER ARM";
        partsName[54] = "3.10 ROCKER ARM SPRING";
        partsName[55] = "3.11 HYDRAULIC LASH ADJUSTSTER";
        partsName[56] = "3.12 CAMSHAFT PULLEY";
        partsName[57] = "3.13 THRUST PLATE";
        partsName[58] = "3.14 CAMSHAFT";
        partsName[59] = "3.15 CYLINDER HEAD BOLTS";
        partsName[60] = "3.16 CYLINDER HEAD";
        partsName[61] = "3.17 CYLINDER HEAD GASKET";
        partsName[62] = "3.18 VALVE SPRING";
        partsName[63] = "3.19 VALVE KEEPER";
        partsName[64] = "3.20 VALVE SPRING SEAT UPPER";
        partsName[65] = "3.21 VALVE SPRING SEAT LOWER";
        partsName[66] = "3.22 VALVE";
        partsName[67] = "3.23 VALVE SEAL";
        partsName[68] = "3.24 VALVE GUIDE ***";
        partsName[69] = "3.25 CAMSHAFT OIL SEAL";
        partsName[70] = "3.26 FUEL PRESSURE REGULATOR";
        partsName[71] = "3.27 RADIATOR";
        partsName[72] = "3.28 SORT BLOCK";
        partsName[73] = "3.29 PISTON RING(NO.1 COMPRESSION)";
        partsName[74] = "3.30 PISTON RING (NO.2 COMPRESSION)";
        partsName[75] = "3.31 PISTON RING(SIDE RAIL AND EXPANDER)***";
        partsName[76] = "3.32 SNAP RING";
        partsName[77] = "3.33 PISTON PIN";
        partsName[78] = "3.34 CONNECTING ROD BUSHING";
        partsName[79] = "3.35 CONNECTING ROD";
        partsName[80] = "3.36 CONNECTING ROD BEARING";
        partsName[81] = "3.37 CONNECTING ROD CAP";
        partsName[82] = "3.38 ENGINE COOLANT DRAIN PLUG";
        partsName[83] = "3.39 WATER BYPASS HOSE";
        partsName[84] = "3.40 WATER PUMP";
        partsName[85] = "3.41 O RING";
        partsName[86] = "3.42 OIL PUMP";
        partsName[87] = "3.43 OIL SEAL";
        partsName[88] = "3.44 REAR OIL SEAL RATAINER";
        partsName[89] = "3.45 KNOCK SENSOR 1";
        partsName[90] = "3.46 KNOCK SENSOR 2";
        partsName[91] = "3.47 FUEL PIPE SUPPORT";
        partsName[92] = "3.48 UNION NUT";
        partsName[93] = "3.49 OIL PRESSURE SWICH";
        partsName[94] = "3.50 GENERATOR";
        partsName[95] = "3.51 IDLER PULLER";
        partsName[96] = "3.52 CRANKSHAFT OIL SEAL";
        partsName[97] = "3.53 CRANKSHAFT";
        partsName[98] = "3.54 CRANKSHAFT THRUST WASHER";
        partsName[99] = "3.55 MAIN BEARING";
        partsName[100] = "3.56 MAIN BEARING CAP";
        partsName[101] = "3.57 LH MOUNTING BRACKET AND INSULATOR ASSEMBLY";
        partsName[102] = "3.58 OIL FILTER AND BRACKET ASSEMBLY";
        partsName[103] = "3.59 COIL";
        partsName[104] = "3.60 TENSIONING RAIL";
        partsName[105] = "3.61 BALANCE SHAFT CHAIN TENIONING";
        partsName[106] = "3.62 COLLAR BOLT TENSIONING RAIL";
        partsName[107] = "3.63 CHAIN SPROCKET OIL PUMP";
        partsName[108] = "3.64 TENSIONING RAIL OIL PUMP";
        partsName[109] = "3.65 IDLER";
        partsName[110] = "3.66 CAMSHAFT PULLEY";
        partsName[111] = "3.67 CRANKSHAFT PULLEY";
        partsName[112] = "4.1  FLANGE YOKE";
        partsName[113] = "4.2  U-JOINT BEARING PLATE STYLE";
        partsName[114] = "4.3  SLIP YOKE BP STYLE";
        partsName[115] = "4.4  TUBE ";
        partsName[116] = "4.5  TUBE YOKE";
        partsName[117] = "4.6  END YOKE ";
        partsName[118] = "4.7  MIDSHIP SHAFT";
        partsName[119] = "4.8  CENTER BEARING ";
        partsName[120] = "4.9  U-JOINT";
        partsName[121] = "4.10 DIFFERENTIAL";
        partsName[122] = "4.11 AXLE";
        partsName[123] = "4.12 CARRIER";
        partsName[124] = "4.13 RING GEAR ";
        partsName[125] = "4.14 AXLE SHAFT SIDE GEAR";
        partsName[126] = "4.15 AXLE SHAFT ";
        partsName[127] = "4.16 AXLE HOUSING ";
        partsName[128] = "4.17 PINION GEAR";
        partsName[129] = "4.18 PINION SHAFT";
        partsName[130] = "4.19 FUEL INJECTOR";
        partsName[131] = "4.20 OIL PAN";
        partsName[132] = "4.21 OIL PAN BAFFLE PLATE";
        partsName[133] = "4.22 OIL STRAINER ";
        partsName[134] = "4.23 OIL PAN ";
        partsName[135] = "4.24 DRAIN PLUG";
        partsName[136] = "4.25 SPARK PLUG ";
        partsName[137] = "4.26 EXHAUST MANIFOLD";
        partsName[138] = "4.27 PRESSURE RELIEF VALUE";
        partsName[139] = "4.28 INTAKE MANIFOLD";
        partsName[140] = "4.29 INTATE MANIFOLD GASKET";
        partsName[141] = "4.30 EXHAUST MANIFOLD GASKET";
        partsName[142] = "4.31 RUBBER GROMMETS";
        partsName[143] = "4.32 MAIN SEAL";
        partsName[144] = "4.33 CAMSHAFT  FRONT OIL SEALS";
        partsName[145] = "4.34 CYLINDER HEAD GASKET";
        partsName[146] = "4.35 CRANK GEAR IOL SEAL";
        partsName[147] = "4.36 OIL PAN GASKET";
        partsName[148] = "4.37 FRONT CRANK OIL SEAL";
        partsName[149] = "4.38 WATER PUMP GASKET ";
        partsName[150] = "4.39 TIMING BELT DRIVE PULLEY";
        partsName[151] = "4.40 DISTRIBUTOR O-RING";
        partsName[152] = "4.41 CAMS";
        partsName[153] = "4.42 TIMING BELT";
        partsName[154] = "4.43 TIMING CHAIN";
        partsName[155] = "4.44 SLIDE RAIL TIMING GEAR";
        partsName[156] = "4.45 CHAIN SPROCKET EXHAUST CAMSHAFT";
        partsName[157] = "4.46 COLLAR BOLT TENSIONING RAILS ";
        partsName[158] = "4.47 TENSIONING RAIL TIMING GEAR ";
        partsName[159] = "4.48 CHAIN SPROCKET INA INTAKE CAMSHAFT ADJUSTER";
        partsName[160] = "4.49 GUIDE RAIL TIMING GEAR ";
        partsName[161] = "4.50 HYDRAULIC TENSIONER CAMSHAFT CHAIN DRIVE";
        partsName[162] = "4.51 FUEL PUMP ASSEMBLE";
        partsName[163] = "4.52 UNIVERSAL JOINT ";
        partsName[164] = "4.53 DIFFERENTIAL SIDE GEAR";
        partsName[165] = "4.54 SIDE GEAR";
        partsName[166] = "4.55 DIFFERENTIAL CASE";
        partsName[167] = "4.56 BEARING CAP";
        partsName[168] = "4.57 AXLE HOUSING ";
        partsName[169] = "4.58 PINION GEAR";
        partsName[170] = "4.59 RING GEAR ";
        partsName[171] = "4.60 TRANSMISSION";
        partsName[172] = "5.1  PRIMARY RETURN SPRING";
        partsName[173] = "5.2  PRIMARY SHOE";
        partsName[174] = "5.3  SHOE HOLD-DOWN";
        partsName[175] = "5.4  PARKING BRAKE CABLE";
        partsName[176] = "5.5  ADJUSTER LEVER SPRING";
        partsName[177] = "5.6  BACKING PLATE ";
        partsName[178] = "5.7  SECONDARY SHOE RETURN SERING";
        partsName[179] = "5.8  WHEEL CYLINDER ASSEMBLY";
        partsName[180] = "5.9  GEBLE GUIDE";
        partsName[181] = "5.10 PARKING BRAKE STRUT";
        partsName[182] = "5.11 PARKING BRAKE LEVER";
        partsName[183] = "5.12 ADJUSTING CABLE";
        partsName[184] = "5.13 SECONDARY SHOE";
        partsName[185] = "5.14 ADJUSTING LEVER";
        partsName[186] = "5.15 ADJUSTING ASSEMBLY";
        partsName[187] = "5.16 BLEEDER SCREW";
        partsName[188] = "5.17 CALIPER";
        partsName[189] = "5.18 DUST BOOT";
        partsName[190] = "5.19 PISTON ";
        partsName[191] = "5.20 BRAKEPADS";
        partsName[192] = "5.21 ANTI-RATTLE CLIPS";
        partsName[193] = "5.22 ROTOR";
        partsName[194] = "5.23 PISTON RING";
        partsName[195] = "5.24 LOCK PIN";
        partsName[196] = "5.25 PAD CLIP";
        partsName[197] = "5.26 SHIM";
        partsName[198] = "5.27 PIN BOOTS";
        partsName[199] = "5.28 GUIDEPIN";
        partsName[200] = "5.29 CYLINDER BODY";
        partsName[201] = "5.30 BLEEDER CAP";
        partsName[202] = "5.31 MOUNTING BRACKET";
        partsName[203] = "6.1  THERMOSTAT";
        partsName[204] = "6.2  RESERVOIR TANK";
        partsName[205] = "6.3  FUEL TANK ";
        partsName[206] = "6.4  FUEL TANK PRESSURE SENSOR";
        partsName[207] = "6.5  OXYGEN SENSOR ";
        partsName[208] = "6.6  AIR INJECTION CHECK VALVE";
        partsName[209] = "6.7  EGR VALVE";
        partsName[210] = "6.8  PURGE";
        partsName[211] = "6.9  FUEL FILTER";
        partsName[212] = "6.10 FUEL TANK VENT ";
        partsName[213] = "6.11 FUEL ISOLATION VALVE";
        partsName[214] = "6.12 HIGH PRESSURE  PUMP";
        partsName[215] = "6.13 FUEL RAIL";
        partsName[216] = "6.14 FUEL GAUGE";
        partsName[217] = "6.15 HEATER";
        partsName[218] = "6.16 HEATER BLOWER FAN ";
        partsName[219] = "6.17 DRAIN TAP";
        partsName[220] = "6.18 COOLANT TEMPERATURE SENSOR";
        partsName[221] = "6.19 HEATER CONTROL VALVE";
        partsName[222] = "6.20 BLOWER MOTOR ";
        partsName[223] = "6.21 OVERFLOW RECOVERY TANK HOSE";
        partsName[224] = "6.22 COOLANT RESERVOIR";
        partsName[225] = "6.23 THROTTLE BODY";
        partsName[226] = "6.24 COOLANT FAN ";
        partsName[227] = "6.25 RADIATOR SHROUD - FAN SHROUD";
        partsName[228] = "6.26 FUEL ACCUMULATOR";
        partsName[229] = "6.27 MAF SENSOR";
        partsName[230] = "6.28 MAP SENSOR";
        partsName[231] = "6.29 IAT SENSOR";
        partsName[232] = "6.30 O2 SENSOR";
        partsName[233] = "6.31 NOX SENSOR";
        partsName[234] = "6.32 EGT SENSOR";
        partsName[235] = "6.33 EGR SENSOR ";
        partsName[236] = "6.34 DISTRIBUTOR";
        partsName[237] = "6.35 BATTERY";
        partsName[238] = "6.36 WARM-UP REGULATOR";
        partsName[239] = "6.37 CHOKE VALVE";
        partsName[240] = "6.38 OIL CATCH CAN";
        partsName[241] = "6.39 DOWNPIPE";
        partsName[242] = "6.40 IAC VALVE";
        partsName[243] = "6.41 VSV FOR ACIS";
        partsName[244] = "6.42 IGNITER";
        partsName[245] = "6.43 ENGINE NOUNT";
        partsName[246] = "6.44 CIRCUIT";
        partsName[247] = "6.45 CLUTCH CYLINDER";
        partsName[248] = "6.46 BLOW OFF VLAVE";
        partsName[249] = "6.47 INTERCOOLER";
        partsName[250] = "6.48 TURBO";
        partsName[251] = "6.49 OIL RETURN GASKET";
        partsName[252] = "6.50 BOOST SOLENOID VALVE";
    }
    public static void main( String args[]) throws InputMismatchException {
        GPT3Integration gpt3 = new GPT3Integration();
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a prompt: ");
        String userPrompt = scanner.nextLine();

        // Κλήση της μεθόδου για αποστολή αιτήματος στο GPT-3
        String gpt3Response = gpt3.getResponse(userPrompt);

        // Εκτύπωση της απάντησης από το GPT-3
        System.out.println("GPT-3 Response: " + gpt3Response);

        // Κλείσιμο του scanner
        scanner.close();
        App makeArray = new App();
        int key1 = 0;
        Scanner input = new Scanner(System.in);
        System.out.println("Please enter the motor vehicle's Brand, model and year of production");
        System.out.printf("Brand:");
        int c = 0;
        do {
            if (c == 1) {
                c = 0;
            }
            try {
                brand = input.nextLine();
            } catch (InputMismatchException e) {
                System.out.printf("ERROR: Inappropriate argument passed into the system, please enter a valid argument.");
                input.nextLine();
                c = 1;
            }
        } while(c == 1);
        System.out.printf("\nModel:");
        do {
            if (c == 1) {
                c = 0;
            }
            try {
                model = input.nextLine();
            } catch (InputMismatchException e) {
                System.out.printf("ERROR: Inappropriate argument passed into the system, please enter a valid argument.");
                input.nextLine();
                c = 1;
            }
        } while(c == 1);
        System.out.printf("\nYear of production:");
        do {
            if (c == 1) {
                c = 0;
            }
            try {
                productionYear = input.nextInt();
            } catch (InputMismatchException e) {
                System.out.printf("ERROR: Inappropriate argument passed into the system, please enter a valid argument.");
                input.nextLine();
                c = 1;
            }
            if (productionYear < 1886) {
            c = 1;
            }
        } while(c == 1);
        System.out.printf("\n");
        for(;;) {
            System.out.printf("Please enter \"1\" or \"2\" to choose an option:\n1) MAIN MENU\n2) SEARCH BAR\n");
            do {
                try {
                    key1 = input.nextInt();
                } catch (InputMismatchException e) {
                    System.out.printf("ERROR: Inappropriate argument passed into the system\nplease enter one " + 
                    "of the accepted values ass following:\n \"1\" or\"2\"\n");
                    input.nextLine();
                }
                if (key1 == 0) {
                    continue;
                }else if (key1 != 1 && key1 != 2) {
                    System.out.printf("Please enter one of the accepted values ass following:\n \"1\" or\"2\"\n");
                }
            } while (key1 != 1 && key1 != 2);
            String key3;
            Scanner k = new Scanner(System.in);
            if (key1 == 1) {
                int key2 = 0;
                System.out.printf("Please enter \"1\", \"2\", \"3\", \"4\", \"5\" or \"6\" to select a category:\n" +
                "1) STEERING PARTS\n2) CLUTCH PARTS\n3) ENGINE PARTS\n4) PROPELLER SHAFT\n5) BRAKE PARTS\n6) EXTRA\n");
                do {
                    try {
                    key2 = input.nextInt();
                    } catch (InputMismatchException e) {
                    System.out.printf("ERROR: Inappropriate argument passed into the system\nplease enter one " +
                    "of the accepted values ass following:\n \"1\", \"2\", \"3\", \"4\", \"5\" or \"6\"\n");
                    input.nextLine();
                    }
                    if (key2 < 1 && key2 > 6) {
                        System.out.println("Please enter one of the accepted values ass following:\n" +
                        "\"1\", \"2\", \"3\", \"4\", \"5\", \"6\"");
                    }
                }
                while (key2 < 1 || key2 > 6);
                System.out.println("Please enter the number of the part you want to select.");
                if (key2 == 1) {
                    System.out.println("1.1 UPPER CONTROL ARM\n1.2 UPPER BALL JOINT\n1.3 COIL SPRING\n" +
                    "1.4 SNOCK ABSORBER\n1.5 LOWER BALL JOINT\n1.6 LOWER CONTROL ARM\n" +
                    "1.7 CONTROL ARM BUSHINGS\n1.8 STABILIZER LINK\n1.9 IDLER ARM\n" +
                    "1.10 INNER TIE-ROD END\n1.11 CENTER LINK\n1.12 PITMAN ARM\n" +
                    "1.13 ADJUSTING SLEEVE\n1.14 OUTER TIE-ROD END\n1.15 STEERING KNUCKLE\n" +
                    "1.16 POWER STEERING PUMP\n1.17 POWER STEERING GEARBOX\n" +
                    "1.18 ANTI-SWAY BAR\n1.19 BALL JOINT\n1.20 UPPER MOUNTING PLATE-BEARING\n" +
                    "1.21 MACPHERSON STRUT\n1.22 BELLOWS\n1.23 RACK-PINION UNIT\n1.24 RACK-PINION BUSHINGS\n" +
                    "1.25 INNER SCOKET ASSEMBLY\n1.26 WHEEL HUB\n1.27 WHEEL BEARING\n1.28 POWER STEERING");
                }else if (key2 == 2) {
                    System.out.println("2.1 SPIGOT BEARING\n2.2 RETAINING SPRING WITH PREFORMED FINGERS\n" +
                    "2.3 RELEAS RING\n2.4 RETAINING SPRING\n2.5 BALL PIN FOR CLUCH FORK\n2.6 FLYWHEEL\n" +
                    "2.7 DRIVE DISC\n2.8 PRESSURE PLATE\n2.9 INNER FULCRUM RING\n2.10 OUTER FULCRUM RING" +
                    "2.11 CLUTCH COVER\n2.12 RELEASE FORK\n2.13 RETURN SPRING OF RELEASE FORK\n2.14 RELEASE BEARING" +
                    "2.15 DIAPHRAGM SPRING\n2.16 PILOT BUSHING\n2.17 BELLHOUSING");
                }else if (key2 == 3) {
                    System.out.println("3.1 FUEL PUMP\n3.2 CYLINDER HEAD COVER\n3.3 GASKET\n" + 
                    "3.4 THERMOSTAT COVER AND GASKET\n3.5 THERMOSTAT\n 3.6 HEAT GAUGE UNIT\n" + 
                    "3.7 BRACKET\n3.8 ROCKER ARM AND SHAFT ASSEMBLE\n3.9 ROCKER ARM\n" + 
                    "3.10 ROCKER ARM SPRING\n3.11 HYDRAULIC LASH ADJUSTSTER\n3.12 CAMSHAFT PULLEY\n" + 
                    "3.13 THRUST PLATE\n3.14 CAMSHAFT\n3.15 CYLINDER HEAD BOLTS\n3.16 CYLINDER HEAD\n" + 
                    "3.17 CYLINDER HEAD GASKET\n3.18 VALVE SPRING\n3.19 VALVE KEEPER\n3.20 VALVE SPRING SEAT UPPER\n" + 
                    "3.21 VALVE SPRING SEAT LOWER\n3.22 VALVE\n3.23 VALVE SEAL\n3.24 VALVE GUIDE ***\n3.25 CAMSHAFT OIL SEAL\n" + 
                    "3.26 FUEL PRESSURE REGULATOR\n3.27 RADIATOR\n3.28 SORT BLOCK\n3.29 PISTON RING(NO.1 COMPRESSION)\n3.30 PISTON RING (NO.2 COMPRESSION)\n" + 
                    "3.31 PISTON RING(SIDE RAIL AND EXPANDER)***\n3.32 SNAP RING\n3.33 PISTON PIN\n3.34 CONNECTING ROD BUSHING\n3.35 CONNECTING ROD\n" + 
                    "3.36 CONNECTING ROD BEARING\n3.37 CONNECTING ROD CAP\n3.38 ENGINE COOLANT DRAIN PLUG\n3.39 WATER BYPASS HOSE\n3.40 WATER PUMP\n" + 
                    "3.41 O RING\n3.42 OIL PUMP\n3.43 OIL SEAL\n3.44 REAR OIL SEAL RATAINER\n3.45 KNOCK SENSOR 1\n3.46 KNOCK SENSOR 2\n3.47 FUEL PIPE SUPPORT\n" + 
                    "3.48 UNION NUT\n3.49 OIL PRESSURE SWICH\n3.50 GENERATOR\n3.51 IDLER PULLER\n3.52 CRANKSHAFT OIL SEAL\n3.53 CRANKSHAFT\n3.54 CRANKSHAFT THRUST WASHER\n" + 
                    "3.55 MAIN BEARING\n3.56 MAIN BEARING CAP\n3.57 LH MOUNTING BRACKET AND INSULATOR ASSEMBLY\n3.58 OIL FILTER AND BRACKET ASSEMBLY\n3.59 COIL\n" + 
                    "3.60 TENSIONING RAIL\n3.61 BALANCE SHAFT CHAIN TENIONING\n3.62 COLLAR BOLT TENSIONING RAIL\n3.63 CHAIN SPROCKET OIL PUMP\n3.64 TENSIONING RAIL OIL PUMP\n" + 
                    "3.65 IDLER\n3.66 CAMSHAFT PULLEY\n3.67 CRANKSHAFT PULLEY");  
                }else if (key2 == 4) {
                    System.out.println("4.1 FLANGE YOKE\n4.2 U-JOINT BEARING PLATE STYLE\n4.3 SLIP YOKE BP STYLE\n4.4 TUBE\n" + 
                    "4.5 TUBE YOKE\n4.6 END YOKE\n4.7 MIDSHIP SHAFT\n4.8 CENTER BEARING\n4.9 U-JOINT\n" + 
                    "4.10 DIFFERENTIAL\n4.11 AXLE\n4.12 CARRIER\n4.13 RING GEAR\n4.14 AXLE SHAFT SIDE GEAR\n" + 
                    "4.15 AXLE SHAFT\n4.16 AXLE HOUSING\n4.17 PINION GEAR\n4.18 PINION SHAFT\n4.19 FUEL INJECTOR\n" + 
                    "4.20 OIL PAN\n4.21 OIL PAN BAFFLE PLATE\n4.22 OIL STRAINER\n4.23 OIL PAN\n4.24 DRAIN PLUG\n" + 
                    "4.25 SPARK PLUG\n4.26 EXHAUST MANIFOLD\n4.27 PRESSURE RELIEF VALUE\n4.28 INTAKE MANIFOLD\n" + 
                    "4.29 INTATE MANIFOLD GASKET\n4.30 EXHAUST MANIFOLD GASKET\n4.31 RUBBER GROMMETS\n4.32 MAIN SEAL\n" + 
                    "4.33 CAMSHAFT  FRONT OIL SEALS\n4.34 CYLINDER HEAD GASKET\n4.35 CRANK GEAR IOL SEAL\n4.36 OIL PAN GASKET\n" +
                    "4.37 FRONT CRANK OIL SEAL\n4.38 WATER PUMP GASKET\n4.39 TIMING BELT DRIVE PULLEY\n4.40 DISTRIBUTOR O-RING\n" +
                    "4.41 CAMS\n4.42 TIMING BELT\n4.43 TIMING CHAIN\n4.44 SLIDE RAIL TIMING GEAR\n4.45 CHAIN SPROCKET EXHAUST CAMSHAFT\n" +
                    "4.46 COLLAR BOLT TENSIONING RAILS\n4.47 TENSIONING RAIL TIMING GEAR\n4.48 CHAIN SPROCKET INA INTAKE CAMSHAFT ADJUSTER\n" +
                    "4.49 GUIDE RAIL TIMING GEAR\n4.50 HYDRAULIC TENSIONER CAMSHAFT CHAIN DRIVE\n4.51 FUEL PUMP ASSEMBLE\n4.52 UNIVERSAL JOINT\n" +
                    "4.53 DIFFERENTIAL SIDE GEAR\n4.54 SIDE GEAR\n4.55 DIFFERENTIAL CASE\n4.56 BEARING CAP\n4.57 AXLE HOUSING\n4.58 PINION GEAR\n" +
                    "4.59 RING GEAR\n4.60 TRANSMISSION");
                }else if (key2 == 5) {
                    System.out.println("5.1 PRIMARY RETURN SPRING\n5.2 PRIMARY SHOE\n5.3 SHOE HOLD-DOWN\n5.4 PARKING BRAKE CABLE\n5.5 ADJUSTER LEVER SPRING\n" + 
                    "5.6 BACKING PLATE\n5.7 SECONDARY SHOE RETURN SERING\n5.8 WHEEL CYLINDER ASSEMBLY\n5.9 GEBLE GUIDE\n5.10 PARKING BRAKE STRUT\n" +
                    "5.11 PARKING BRAKE LEVER\n5.12 ADJUSTING CABLE\n5.13 SECONDARY SHOE\n5.14 ADJUSTING LEVER\n5.15 ADJUSTING ASSEMBLY\n" + 
                    "5.16 BLEEDER SCREW\n5.17 CALIPER\n5.18 DUST BOOT\n5.19 PISTON\n5.20 BRAKEPADS\n5.21 ANTI-RATTLE CLIPS\n5.22 ROTOR\n" + 
                    "5.23 PISTON RING\n5.24 LOCK PIN\n5.25 PAD CLIP\n5.26 SHIM\n5.27 PIN BOOTS\n5.28 GUIDEPIN\n5.29 CYLINDER BODY\n" + 
                    "5.30 BLEEDER CAP\n5.31 MOUNTING BRACKET");
                }else if (key2 == 6) {
                    System.out.println("6.1 THERMOSTAT\n6.2 RESERVOIR TANK\n6.3 FUEL TANK\n6.4 FUEL TANK PRESSURE SENSOR\n6.5 OXYGEN SENSOR\n" +
                    "6.6 AIR INJECTION CHECK VALVE\n6.7 EGR VALVE\n6.8 PURGE\n6.9 FUEL FILTER\n6.10 FUEL TANK VENT\n6.11 FUEL ISOLATION VALVE\n" +
                    "6.12 HIGH PRESSURE PUMP\n6.13 FUEL RAIL\n6.14 FUEL GAUGE\n6.15 HEATER\n6.16 HEATER BLOWER FAN\n6.17 DRAIN TAP\n" +
                    "6.18 COOLANT TEMPERATURE SENSOR\n6.19 HEATER CONTROL VALVE\n6.20 BLOWER MOTOR\n6.21 OVERFLOW RECOVERY TANK HOSE\n" +
                    "6.22 COOLANT RESERVOIR\n6.23 THROTTLE BODY\n6.24 COOLANT FAN \n6.25 RADIATOR SHROUD - FAN SHROUD\n6.26 FUEL ACCUMULATOR\n" +
                    "6.27 MAF SENSOR\n6.28 MAP SENSOR\n6.29 IAT SENSOR\n6.30 O2 SENSOR\n6.31 NOX SENSOR\n6.32 EGT SENSOR\n6.33 EGR SENSOR\n" + 
                    "6.34 DISTRIBUTOR\n6.35 BATTERY\n6.36 WARM-UP REGULATOR\n6.37 CHOKE VALVE\n6.38 OIL CATCH CAN\n6.39 DOWNPIPE\n6.40 IAC VALVE\n" + 
                    "6.41 VSV FOR ACIS\n6.42 IGNITER\n6.43 ENGINE NOUNT\n6.44 CIRCUIT\n6.45 CLUTCH CYLINDER\n6.46 BLOW OFF VLAVE\n6.47 INTERCOOLER\n" +
                    "6.48 TURBO\n6.49 OIL RETURN GASKET\n6.50 BOOST SOLENOID VALVE");
                }
                do {
                    key3 = k.nextLine();
                } while (key3 != "1.1" && key3 != "1.2" && key3 != "1.3" && key3 != "1.4" && key3 != "1.5" && key3 != "1.6" &&
                    key3 != "1.7" && key3 != "1.8" && key3 != "1.9" && key3 != "1.10" && key3 != "1.11" && key3 != "1.12" &&
                    key3 != "1.13" && key3 != "1.14" && key3 != "1.15" && key3 != "1.16" && key3 != "1.17" && key3 != "1.18" &&
                    key3 != "1.19" && key3 != "1.20" && key3 != "1.21" && key3 != "1.22" && key3 != "1.23" && key3 != "1.24" &&
                    key3 != "1.25" && key3 != "1.26" && key3 != "1.27" && key3 != "1.28" && key3 != "2.1" && key3 != "2.2" &&
                    key3 != "2.3" && key3 != "2.4" && key3 != "2.5" && key3 != "2.6" && key3 != "2.7" && key3 != "2.8" &&
                    key3 != "2.9" && key3 != "2.10" && key3 != "2.11" && key3 != "2.12" && key3 != "2.13" && key3 != "2.14" &&
                    key3 != "2.15" && key3 != "2.16" && key3 != "2.17" && key3 != "3.1" && key3 != "3.2" && key3 != "3.3" &&
                    key3 != "3.4" && key3 != "3.5" && key3 != "3.6" && key3 != "3.7" && key3 != "3.8" && key3 != "3.9" &&
                    key3 != "3.10" && key3 != "3.11" && key3 != "3.12" && key3 != "3.13" && key3 != "3.14" && key3 != "3.15" &&
                    key3 != "3.16" && key3 != "3.17" && key3 != "3.18" && key3 != "3.19" && key3 != "3.20" && key3 != "3.21" &&
                    key3 != "3.22" && key3 != "3.23" && key3 != "3.24" && key3 != "3.25" && key3 != "3.26" && key3 != "3.27" &&
                    key3 != "3.28" && key3 != "3.29" && key3 != "3.30" && key3 != "3.31" && key3 != "3.32" && key3 != "3.33" &&
                    key3 != "3.34" && key3 != "3.35" && key3 != "3.36" && key3 != "3.37" && key3 != "3.38" && key3 != "3.39" &&
                    key3 != "3.40" && key3 != "3.41" && key3 != "3.42" && key3 != "3.43" && key3 != "3.44" && key3 != "3.45" &&
                    key3 != "3.46" && key3 != "3.47" && key3 != "3.48" && key3 != "3.49" && key3 != "3.50" && key3 != "3.51" &&
                    key3 != "3.52" && key3 != "3.53" && key3 != "3.54" && key3 != "3.55" && key3 != "3.56" && key3 != "3.57" &&
                    key3 != "3.58" && key3 != "3.59" && key3 != "3.60" && key3 != "3.61" && key3 != "3.62" && key3 != "3.63" &&
                    key3 != "3.64" && key3 != "3.65" && key3 != "3.66" && key3 != "3.67" && key3 != "4.1" && key3 != "4.2" &&
                    key3 != "4.3" && key3 != "4.4" && key3 != "4.5" && key3 != "4.6" && key3 != "4.7" && key3 != "4.8" &&
                    key3 != "4.9" && key3 != "4.10" && key3 != "4.11" && key3 != "4.12" && key3 != "4.13" && key3 != "4.14" &&
                    key3 != "4.15" && key3 != "4.16" && key3 != "4.17" && key3 != "4.18" && key3 != "4.19" && key3 != "4.20" &&
                    key3 != "4.21" && key3 != "4.22" && key3 != "4.23" && key3 != "4.24" && key3 != "4.25" && key3 != "4.26" &&
                    key3 != "4.27" && key3 != "4.28" && key3 != "4.29" && key3 != "4.30" && key3 != "4.31" && key3 != "4.32" &&
                    key3 != "4.33" && key3 != "4.34" && key3 != "4.35" && key3 != "4.36" && key3 != "4.37" && key3 != "4.38" &&
                    key3 != "4.39" && key3 != "4.40" && key3 != "4.41" && key3 != "4.42" && key3 != "4.43" && key3 != "4.44" &&
                    key3 != "4.45" && key3 != "4.46" && key3 != "4.47" && key3 != "4.48" && key3 != "4.49" && key3 != "4.50" &&
                    key3 != "4.51" && key3 != "4.52" && key3 != "4.53" && key3 != "4.54" && key3 != "4.55" && key3 != "4.56" &&
                    key3 != "4.57" && key3 != "4.58" && key3 != "4.59" && key3 != "4.60" && key3 != "5.1" && key3 != "5.2" &&
                    key3 != "5.3" && key3 != "5.4" && key3 != "5.5" && key3 != "5.6" && key3 != "5.7" && key3 != "5.8" &&
                    key3 != "5.9" && key3 != "5.10" && key3 != "5.11" && key3 != "5.12" && key3 != "5.13" && key3 != "5.14" &&
                    key3 != "5.15" && key3 != "5.16" && key3 != "5.17" && key3 != "5.18" && key3 != "5.19" && key3 != "5.20" &&
                    key3 != "5.21" && key3 != "5.22" && key3 != "5.23" && key3 != "5.24" && key3 != "5.25" && key3 != "5.26" &&
                    key3 != "5.27" && key3 != "5.28" && key3 != "5.29" && key3 != "5.30" && key3 != "5.31" && key3 != "6.1" &&
                    key3 != "6.2" && key3 != "6.3" && key3 != "6.4" && key3 != "6.5" && key3 != "6.6" && key3 != "6.7" &&
                    key3 != "6.8" && key3 != "6.9" && key3 != "6.10" && key3 != "6.11" && key3 != "6.12" && key3 != "6.13" &&
                    key3 != "6.14" && key3 != "6.15" && key3 != "6.16" && key3 != "6.17" && key3 != "6.18" && key3 != "6.19" &&
                    key3 != "6.20" && key3 != "6.21" && key3 != "6.22" && key3 != "6.23" && key3 != "6.24" && key3 != "6.25" &&
                    key3 != "6.26" && key3 != "6.27" && key3 != "6.28" && key3 != "6.29" && key3 != "6.30" && key3 != "6.31" &&
                    key3 != "6.32" && key3 != "6.33" && key3 != "6.34" && key3 != "6.35" && key3 != "6.36" && key3 != "6.37" &&
                    key3 != "6.38" && key3 != "6.39" && key3 != "6.40" && key3 != "6.41" && key3 != "6.42" && key3 != "6.43" &&
                    key3 != "6.44" && key3 != "6.45" && key3 != "6.46" && key3 != "6.47" && key3 != "6.48" && key3 != "6.49" &&
                    key3 != "6.50");
                k.close();
                return;
            } else {
                do {
                    System.out.printf("SEARCH:");
                    key3 = k.nextLine();
                } while (!key3.equals("UPPER CONTROL ARM") && !key3.equals("UPPER BALL JOINT") && !key3.equals("COIL SPRING") && !key3.equals("SNOCK ABSORBER") && !key3.equals("LOWER BALL JOINT") && !key3.equals("LOWER CONTROL ARM") &&
                !key3.equals("CONTROL ARM BUSHINGS") && !key3.equals("STABILIZER LINK") && !key3.equals("IDLER ARM") && !key3.equals("INNER TIE-ROD END") && !key3.equals("CENTER LINK") && !key3.equals("PITMAN ARM") &&
                !key3.equals("ADJUSTING SLEEVE") && !key3.equals("OUTER TIE-ROD END") && !key3.equals("STEERING KNUCKLE") && !key3.equals("POWER STEERING PUMP") && !key3.equals("POWER STEERING GEARBOX") && !key3.equals("ANTI-SWAY BAR") &&
                !key3.equals("BALL JOINT") && !key3.equals("UPPER MOUNTING PLATE-BEARING") && !key3.equals("MACPHERSON STRUT") && !key3.equals("BELLOWS") && !key3.equals("RACK-PINION UNIT") && !key3.equals("RACK-PINION BUSHINGS") &&
                !key3.equals("INNER SCOKET ASSEMBLY") && !key3.equals("WHEEL HUB") && !key3.equals("WHEEL BEARING") && !key3.equals("POWER STEERING") && !key3.equals("SPIGOT BEARING") && !key3.equals("RETAINING SPRING WITH PREFORMED FINGERS") &&
                !key3.equals("RELEAS RING") && !key3.equals("RETAINING SPRING") && !key3.equals("BALL PIN FOR CLUCH FORK") && !key3.equals("FLYWHEEL") && !key3.equals("DRIVE DISC") && !key3.equals("PRESSURE PLATE") &&
                !key3.equals("INNER FULCRUM RING") && !key3.equals("OUTER FULCRUM RING") && !key3.equals("CLUTCH COVER") && !key3.equals("RELEASE FORK") && !key3.equals("RETURN SPRING OF RELEASE FORK") && !key3.equals("RELEASE BEARING") &&
                !key3.equals("DIAPHRAGM SPRING") && !key3.equals("PILOT BUSHING") && !key3.equals("BELLHOUSING") && !key3.equals("FUEL PUMP") && !key3.equals("CYLINDER HEAD COVER") && !key3.equals("GASKET") &&
                !key3.equals("THERMOSTAT COVER AND GASKET") && !key3.equals("THERMOSTAT") && !key3.equals("HEAT GAUGE UNIT") && !key3.equals("BRACKET") && !key3.equals("ROCKER ARM AND SHAFT ASSEMBLE") && !key3.equals("ROCKER ARM") &&
                !key3.equals("ROCKER ARM SPRING") && !key3.equals("HYDRAULIC LASH ADJUSTSTER") && !key3.equals("CAMSHAFT PULLEY") && !key3.equals("THRUST PLATE") && !key3.equals("CAMSHAFT") && !key3.equals("CYLINDER HEAD BOLTS") &&
                !key3.equals("CYLINDER HEAD") && !key3.equals("CYLINDER HEAD GASKET") && !key3.equals("VALVE SPRING") && !key3.equals("VALVE KEEPER") && !key3.equals("VALVE SPRING SEAT UPPER") && !key3.equals("VALVE SPRING SEAT LOWER") &&
                !key3.equals("VALVE") && !key3.equals("VALVE SEAL") && !key3.equals("VALVE GUIDE") && !key3.equals("CAMSHAFT OIL SEAL") && !key3.equals("FUEL PRESSURE REGULATOR") && !key3.equals("RADIATOR") &&
                !key3.equals("SORT BLOCK") && !key3.equals("PISTON RING(NO.1 COMPRESSION)") && !key3.equals("PISTON RING(NO.2 COMPRESSION)") && !key3.equals("PISTON RING(SIDE RAIL AND EXPANDER)") && !key3.equals("SNAP RING ") && !key3.equals("PISTON PIN") &&
                !key3.equals("CONNECTING ROD BUSHING") && !key3.equals("CONNECTING ROD") && !key3.equals("CONNECTING ROD BEARING") && !key3.equals("CONNECTING ROD CAP") && !key3.equals("ENGINE COOLANT DRAIN PLUG") && !key3.equals("WATER BYPASS HOSE") &&
                !key3.equals("WATER PUMP") && !key3.equals("O-RING") && !key3.equals("OIL PUMP") && !key3.equals("OIL SEAL") && !key3.equals("REAR OIL SEAL RATAINER") && !key3.equals("KNOCK SENSOR 1") &&
                !key3.equals("KNOCK SENSOR 2") && !key3.equals("FUEL PIPE SUPPORT") && !key3.equals("UNION NUT") && !key3.equals("OIL PRESSURE SWITCH") && !key3.equals("GENERATOR") && !key3.equals("IDLER PULLER") &&
                !key3.equals("CRANKSHAFT OIL SEAL") && !key3.equals("CRANKSHAFT") && !key3.equals("CRANKSHAFT THRUST WASHER") && !key3.equals("MAIN BEARING") && !key3.equals("MAIN BEARING CAP") && !key3.equals("LH ENGINE MOUNTING BRACKET AND INSULATOR ASSEMBLY") &&
                !key3.equals("OIL FILTER AND BRACKET ASSEMBLY") && !key3.equals("OIL LEVEL SENSOR") && !key3.equals("COIL") && !key3.equals("TENSIONING  RAIL") && !key3.equals("BALANCE SHAFT CHAIN TENIONING") && !key3.equals("COLLAR BOLT TENSIONING RAIL") &&
                !key3.equals("CHAIN SPROCKET OIL PUMP") && !key3.equals("TENSIONING RAIL OIL PUMP") && !key3.equals("IDLER") && !key3.equals("CAMSHAFT PULLEY") && !key3.equals("CRANKSHAFT PULLEY") && !key3.equals("PROPELLER SHAFT") &&
                !key3.equals("FLANGE YOKE") && !key3.equals("U-JOINT BEARING PLATE STYLE") && !key3.equals("SLIP YOKE BP STYLE") && !key3.equals("TUBE") && !key3.equals("TUBE YOKE") && !key3.equals("END YOKE") &&
                !key3.equals("MIDSHIP SHAFT") && !key3.equals("CENTER BEARING") && !key3.equals("U-JOINT") && !key3.equals("DIFFERENTIAL") && !key3.equals("AXLE") && !key3.equals("CARRIER") &&
                !key3.equals("RING GEAR") && !key3.equals("AXLE SHAFT SIDE GEAR") && !key3.equals("AXLE SHAFT") && !key3.equals("AXLE HOUSING") && !key3.equals("PINION GEAR") && !key3.equals("PINION SHAFT") &&
                !key3.equals("FUEL INJECTOR") && !key3.equals("OIL PAN") && !key3.equals("OIL PAN BAFFLE PLATE") && !key3.equals("OIL STRAINER ") && !key3.equals("OIL PAN") && !key3.equals("DRAIN PLUG") &&
                !key3.equals("SPARK PLUG") && !key3.equals("EXHAUST MANIFOLD") && !key3.equals("PRESSURE RELIEF VALUE") && !key3.equals("INTAKE MANIFOLD") && !key3.equals("INTATE MANIFOLD GASKET") && !key3.equals("EXHAUST MANIFOLD GASKET") &&
                !key3.equals("RUBBER GROMMETS") && !key3.equals("MAIN SEAL") && !key3.equals("CAMSHAFT  FRONT OIL SEALS") && !key3.equals("CYLINDER HEAD GASKET") && !key3.equals("CRANK GEAR IOL SEAL") && !key3.equals("OIL PAN GASKET") &&
                !key3.equals("FRONT CRANK OIL SEAL") && !key3.equals("WATER PUMP GASKET") && !key3.equals("TIMING BELT DRIVE PULLEY") && !key3.equals("DISTRIBUTOR O-RING") && !key3.equals("CAMS") && !key3.equals("TIMING BELT") &&
                !key3.equals("TIMING CHAIN") && !key3.equals("SLIDE RAIL TIMING GEAR") && !key3.equals("CHAIN SPROCKET EXHAUST CAMSHAFT") && !key3.equals("COLLAR BOLT TENSIONING RAILS") && !key3.equals("TENSIONING RAIL TIMING GEAR") && !key3.equals("CHAIN SPROCKET INA INTAKE CAMSHAFT ADJUSTER") &&
                !key3.equals("GUIDE RAIL TIMING GEAR") && !key3.equals("HYDRAULIC TENSIONER CAMSHAFT CHAIN DRIVE") && !key3.equals("FUEL PUMP ASSEMBLE") && !key3.equals("UNIVERSAL JOINT") && !key3.equals("DIFFERENTIAL SIDE GEAR") && !key3.equals("SIDE GEAR") &&
                !key3.equals("DIFFERENTIAL CASE") && !key3.equals("BEARING CAP") && !key3.equals("AXLE HOUSING") && !key3.equals("PINION GEAR") && !key3.equals("RING GEAR") && !key3.equals("TRANSMISSION") &&
                !key3.equals("PRIMARY RETURN SPRING") && !key3.equals("PRIMARY SHOE") && !key3.equals("SHOE HOLD-DOWN") && !key3.equals("PARKING BRAKE CABLE") && !key3.equals("ADJUSTER LEVER SPRING") && !key3.equals("BACKING PLATE") &&
                !key3.equals("SECONDARY SHOE RETURN SERING") && !key3.equals("WHEEL CYLINDER ASSEMBLY") && !key3.equals("GEBLE GUIDE") && !key3.equals("PARKING BRAKE STRUT") && !key3.equals("PARKING BRAKE LEVER") && !key3.equals("ADJUSTING CABLE") &&
                !key3.equals("SECONDARY SHOE") && !key3.equals("ADJUSTING LEVER") && !key3.equals("ADJUSTING ASSEMBLY") && !key3.equals("BLEEDER SCREW") && !key3.equals("CALIPER") && !key3.equals("DUST BOOT") &&
                !key3.equals("PISTON") && !key3.equals("BRAKEPADS") && !key3.equals("ANTI-RATTLE CLIPS") && !key3.equals("ROTOR") && !key3.equals("PISTON RING") && !key3.equals("LOCK PIN") &&
                !key3.equals("PAD CLIP") && !key3.equals("SHIM") && !key3.equals("PIN BOOTS") && !key3.equals("GUIDEPIN") && !key3.equals("CYLINDER BODY") && !key3.equals("BLEEDER CAP") &&
                !key3.equals("MOUNTING BRACKET") && !key3.equals("THERMOSTAT") && !key3.equals("RESERVOIR TANK") && !key3.equals("FUEL TANK") && !key3.equals("FUEL TANK PRESSURE SENSOR") && !key3.equals("OXYGEN SENSOR") &&
                !key3.equals("AIR INJECTION CHECK VALVE") && !key3.equals("EGR VALVE") && !key3.equals("PURGE") && !key3.equals("FUEL FILTER") && !key3.equals("FUEL TANK VENT") && !key3.equals("FUEL ISOLATION VALVE") &&
                !key3.equals("HIGH PRESSURE  PUMP") && !key3.equals("FUEL RAIL") && !key3.equals("FUEL GAUGE") && !key3.equals("HEATER") && !key3.equals("HEATER BLOWER FAN") && !key3.equals("DRAIN TAP") &&
                !key3.equals("COOLANT TEMPERATURE SENSOR") && !key3.equals("HEATER CONTROL VALVE") && !key3.equals("BLOWER MOTOR") && !key3.equals("OVERFLOW RECOVERY TANK HOSE") && !key3.equals("COOLANT RESERVOIR") && !key3.equals("THROTTLE BODY") &&
                !key3.equals("COOLANT FAN") && !key3.equals("RADIATOR SHROUD - FAN SHROUD") && !key3.equals("FUEL ACCUMULATOR") && !key3.equals("MAF SENSOR") && !key3.equals("MAP SENSOR") && !key3.equals("IAT SENSOR") &&
                !key3.equals("O2 SENSOR") && !key3.equals("NOX SENSOR") && !key3.equals("EGT SENSOR") && !key3.equals("EGR SENSOR") && !key3.equals("DISTRIBUTOR") && !key3.equals("BATTERY") &&
                !key3.equals("WARM-UP REGULATOR") && !key3.equals("CHOKE VALVE") && !key3.equals("OIL CATCH CAN") && !key3.equals("DOWNPIPE") && !key3.equals("IAC VALVE") && !key3.equals("VSV FOR ACIS") &&
                !key3.equals("IGNITER") && !key3.equals("ENGINE NOUNT") && !key3.equals("CIRCUIT") && !key3.equals("CLUTCH CYLINDER") && !key3.equals("BLOW OFF VLAVE") && !key3.equals("INTERCOOLER") &&
                !key3.equals("TURBO") && !key3.equals("OIL RETURN GASKET") && !key3.equals("BOOST SOLENOID VALVE"));
                System.out.printf("\n");
                int i = 0;
                boolean flag = false;
                int choice;
                while (flag == false) {
                    if (partsName[i] == key3) {
                        flag = true;
                        choice = i;
                    }
                }
                input.close();
                return;
            }
        }
    }
}
